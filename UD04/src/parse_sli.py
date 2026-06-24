#!/usr/bin/env python3
"""Parse JSON logs and produce a minimal SLI report."""

import json
import sys
from collections import Counter
from pathlib import Path


def percentile(values, p):
    if not values:
        return None
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * (p / 100)))
    return ordered[index]


def load_records(path: Path):
    records = []
    bad_lines = 0
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                bad_lines += 1
    return records, bad_lines


def main():
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("logs/app.log")
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("evidence/sli_report.json")

    records, bad_lines = load_records(log_path)

    durations = [r.get("duration_ms") for r in records if isinstance(r.get("duration_ms"), (int, float))]
    statuses = [r.get("status") for r in records if isinstance(r.get("status"), int)]
    paths = [r.get("path") for r in records if r.get("path")]
    request_ids = [r.get("request_id") for r in records if r.get("request_id")]

    total = len(records)
    errors = sum(1 for s in statuses if s >= 400)
    success = total - errors

    error_rate = round((errors / total) * 100, 2) if total else 0.0
    availability = round((success / total) * 100, 2) if total else 0.0

    report = {
        "source_log": str(log_path),
        "total_requests": total,
        "error_count": errors,
        "error_rate_percent": error_rate,
        "availability_percent": availability,
        "latency_p50_ms": percentile(durations, 50),
        "latency_p95_ms": percentile(durations, 95),
        "latency_max_ms": max(durations) if durations else None,
        "status_breakdown": dict(Counter(str(s) for s in statuses)),
        "top_paths": [
            {"path": path, "count": count}
            for path, count in Counter(paths).most_common(10)
        ],
        "sample_request_ids": request_ids[:10],
        "bad_lines_skipped": bad_lines,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(json.dumps(report, indent=2))
    print(f"Report written to {out_path}")


if __name__ == "__main__":
    main()
