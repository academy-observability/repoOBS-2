#!/usr/bin/env python3
"""Mini log-search tool for UD23.

This is not Kibana. It is a controlled teaching aid that simulates typical
log-stack operations: filter, search, group-by and summary on JSONL logs.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def load_records(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def main():
    parser = argparse.ArgumentParser(description="UD23 JSONL log query helper")
    parser.add_argument("--file", required=True, help="JSONL log file")
    parser.add_argument("--status-min", type=int, default=None, help="Minimum HTTP status")
    parser.add_argument("--contains", default=None, help="Search text in JSON record")
    parser.add_argument("--group-by", default=None, help="Group by a field such as path, service, status")
    parser.add_argument("--summary", action="store_true", help="Print summary")
    parser.add_argument("--limit", type=int, default=20, help="Max records to print")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    records = list(load_records(path))

    if args.status_min is not None:
        records = [r for r in records if int(r.get("status", 0)) >= args.status_min]

    if args.contains:
        needle = args.contains.lower()
        records = [r for r in records if needle in json.dumps(r, ensure_ascii=False).lower()]

    if args.summary:
        print("Total records:", len(records))
        print("By service:", dict(Counter(r.get("service") for r in records)))
        print("By path:", dict(Counter(r.get("path") for r in records)))
        print("By status:", dict(Counter(str(r.get("status")) for r in records)))
        if records:
            avg = sum(float(r.get("latency_ms", 0)) for r in records) / len(records)
            print("Avg latency ms:", round(avg, 2))
        return

    if args.group_by:
        counts = Counter(str(r.get(args.group_by, "<missing>")) for r in records)
        for key, count in counts.most_common():
            print(f"{key}\t{count}")
        return

    for r in records[: args.limit]:
        print(json.dumps(r, ensure_ascii=False))
    if len(records) > args.limit:
        print(f"... {len(records) - args.limit} more records")


if __name__ == "__main__":
    main()
