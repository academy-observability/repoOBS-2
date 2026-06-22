#!/usr/bin/env python3
"""HTTP lab server for OBS_UD03.

Endpoints:
  /        -> 200 text
  /health  -> 200 OK
  /metrics -> 200 simple metrics text
  /slow    -> 200 after a short delay
  /fail    -> 500 simulated error
  other    -> 404
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import time
from datetime import datetime, timezone


class LabHandler(BaseHTTPRequestHandler):
    server_version = "OBSUD03HTTP/1.0"

    def _send_text(self, status: int, body: str, content_type: str = "text/plain; charset=utf-8") -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_HEAD(self) -> None:
        if self.path in ["/", "/health", "/metrics", "/slow"]:
            self.send_response(200)
        elif self.path == "/fail":
            self.send_response(500)
        else:
            self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

    def do_GET(self) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        if self.path == "/":
            self._send_text(200, f"OBS UD03 HTTP lab server\ntime={timestamp}\n")
        elif self.path == "/health":
            self._send_text(200, "OK\n")
        elif self.path == "/metrics":
            self._send_text(
                200,
                "# HELP obs_ud03_requests_total Simulated total requests\n"
                "# TYPE obs_ud03_requests_total counter\n"
                "obs_ud03_requests_total 42\n"
                "# HELP obs_ud03_errors_total Simulated total errors\n"
                "# TYPE obs_ud03_errors_total counter\n"
                "obs_ud03_errors_total 3\n",
            )
        elif self.path == "/slow":
            time.sleep(2)
            self._send_text(200, "slow response completed\n")
        elif self.path == "/fail":
            self._send_text(500, "simulated internal server error\n")
        else:
            self._send_text(404, "not found\n")

    def log_message(self, format: str, *args) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args,
        ))


def parse_port(argv: list[str]) -> int:
    if len(argv) < 2:
        return 8081
    try:
        port = int(argv[1])
    except ValueError as exc:
        raise SystemExit("Porta non valida. Esempio: python3 src/http_lab_server.py 8081") from exc
    if not (1024 <= port <= 65535):
        raise SystemExit("Usare una porta tra 1024 e 65535 per il laboratorio.")
    return port


def main() -> None:
    port = parse_port(sys.argv)
    server = HTTPServer(("0.0.0.0", port), LabHandler)
    print(f"OBS UD03 HTTP lab server in ascolto su http://localhost:{port}")
    print("Endpoint disponibili: /, /health, /metrics, /slow, /fail")
    print("Premere CTRL+C per arrestare il server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer arrestato.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
