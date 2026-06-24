#!/usr/bin/env python3
"""
Servizio HTTP dimostrativo per UD04.

Il servizio usa solo la libreria standard Python per evitare dipendenze esterne.
Espone endpoint semplici, genera log JSON e mantiene metriche minime in memoria.
"""

import json
import os
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", "9100"))
LOG_PATH = os.environ.get("LOG_PATH", "logs/app.log")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "obs-demo")
SERVICE_VERSION = os.environ.get("SERVICE_VERSION", "1.0.0")
READY = os.environ.get("READY", "true").lower() not in {"0", "false", "no"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class MetricsStore:
    def __init__(self):
        self.lock = Lock()
        self.total_requests = 0
        self.total_errors = 0
        self.total_duration_ms = 0
        self.max_duration_ms = 0
        self.path_counts = {}
        self.status_counts = {}

    def record(self, path: str, status: int, duration_ms: int) -> None:
        with self.lock:
            self.total_requests += 1
            if status >= 400:
                self.total_errors += 1
            self.total_duration_ms += duration_ms
            self.max_duration_ms = max(self.max_duration_ms, duration_ms)
            self.path_counts[path] = self.path_counts.get(path, 0) + 1
            status_key = str(status)
            self.status_counts[status_key] = self.status_counts.get(status_key, 0) + 1

    def snapshot(self) -> dict:
        with self.lock:
            avg = 0
            if self.total_requests:
                avg = round(self.total_duration_ms / self.total_requests, 2)
            return {
                "total_requests": self.total_requests,
                "total_errors": self.total_errors,
                "avg_duration_ms": avg,
                "max_duration_ms": self.max_duration_ms,
                "path_counts": dict(self.path_counts),
                "status_counts": dict(self.status_counts),
            }


METRICS = MetricsStore()


def write_log(record: dict) -> None:
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


class Handler(BaseHTTPRequestHandler):
    server_version = "ObservableDemo/1.0"

    def log_message(self, format, *args):
        # Disattiviamo il log standard di BaseHTTPRequestHandler per tenere pulito il terminale.
        return

    def request_id(self) -> str:
        incoming = self.headers.get("X-Request-Id")
        if incoming and incoming.strip():
            return incoming.strip()
        return str(uuid.uuid4())

    def send_json(self, status: int, payload: dict, request_id: str, start_time: float, level: str = "INFO", extra: dict | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-Request-Id", request_id)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self.write_observation(status, request_id, start_time, level=level, extra=extra)

    def send_text(self, status: int, payload: str, request_id: str, start_time: float, content_type: str = "text/plain; charset=utf-8") -> None:
        body = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Request-Id", request_id)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self.write_observation(status, request_id, start_time)

    def write_observation(self, status: int, request_id: str, start_time: float, level: str = "INFO", extra: dict | None = None) -> None:
        duration_ms = int((time.time() - start_time) * 1000)
        parsed = urlparse(self.path)
        record = {
            "ts": utc_now_iso(),
            "level": level,
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "request_id": request_id,
            "client": self.client_address[0],
            "method": self.command,
            "path": parsed.path,
            "query": parsed.query,
            "status": status,
            "duration_ms": duration_ms,
        }
        if extra:
            record.update(extra)
        write_log(record)
        METRICS.record(parsed.path, status, duration_ms)

    def do_GET(self):
        start = time.time()
        rid = self.request_id()
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/health":
            self.send_json(200, {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}, rid, start)
            return

        if path == "/ready":
            if READY:
                self.send_json(200, {"ready": True, "service": SERVICE_NAME}, rid, start)
            else:
                self.send_json(503, {"ready": False, "reason": "READY=false"}, rid, start, level="WARN", extra={"error": "not_ready"})
            return

        if path == "/time":
            self.send_json(200, {"utc": utc_now_iso()}, rid, start)
            return

        if path == "/work":
            requested_ms = query.get("ms", ["100"])[0]
            try:
                delay_ms = max(0, min(int(requested_ms), 2000))
            except ValueError:
                self.send_json(400, {"error": "invalid ms parameter"}, rid, start, level="WARN", extra={"error": "invalid_ms"})
                return
            time.sleep(delay_ms / 1000)
            self.send_json(200, {"worked": True, "delay_ms": delay_ms}, rid, start, extra={"simulated_delay_ms": delay_ms})
            return

        if path == "/fail":
            self.send_json(500, {"error": "simulated failure"}, rid, start, level="ERROR", extra={"error": "simulated_failure"})
            return

        if path == "/metrics":
            snapshot = METRICS.snapshot()
            lines = [
                "# HELP http_requests_total Total HTTP requests handled by the demo service",
                "# TYPE http_requests_total counter",
                f"http_requests_total {snapshot['total_requests']}",
                "# HELP http_errors_total Total HTTP requests with status >= 400",
                "# TYPE http_errors_total counter",
                f"http_errors_total {snapshot['total_errors']}",
                "# HELP http_request_duration_avg_ms Average request duration in milliseconds",
                "# TYPE http_request_duration_avg_ms gauge",
                f"http_request_duration_avg_ms {snapshot['avg_duration_ms']}",
                "# HELP http_request_duration_max_ms Max request duration in milliseconds",
                "# TYPE http_request_duration_max_ms gauge",
                f"http_request_duration_max_ms {snapshot['max_duration_ms']}",
                "",
            ]
            self.send_text(200, "\n".join(lines), rid, start)
            return

        self.send_json(404, {"error": "not found", "path": path}, rid, start, level="WARN", extra={"error": "not_found"})

    def do_POST(self):
        start = time.time()
        rid = self.request_id()
        parsed = urlparse(self.path)

        if parsed.path != "/echo":
            self.send_json(404, {"error": "not found", "path": parsed.path}, rid, start, level="WARN", extra={"error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw) if raw else None
        except Exception:
            self.send_json(400, {"error": "bad json"}, rid, start, level="WARN", extra={"error": "bad_json"})
            return

        self.send_json(200, {"echo": data}, rid, start)


def main() -> None:
    os.makedirs(os.path.dirname(LOG_PATH) or ".", exist_ok=True)
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Serving {SERVICE_NAME} {SERVICE_VERSION} on http://localhost:{PORT}")
    print(f"Log path: {LOG_PATH}")
    print(f"Ready flag: {READY}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nService stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
