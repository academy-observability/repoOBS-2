import json
import os
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "1.0")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_log(status_code: int, message: str = "request_completed") -> None:
    latency_ms = round((time.perf_counter() - g.start_time) * 1000, 2)

    record = {
        "timestamp": utc_now_iso(),
        "level": "INFO" if status_code < 400 else "ERROR",
        "message": message,
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status": int(status_code),
        "latency_ms": latency_ms,
        "client_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
        "version": APP_VERSION,
    }

    print(json.dumps(record), flush=True)


@app.before_request
def before_request() -> None:
    g.start_time = time.perf_counter()
    g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))


@app.after_request
def after_request(response):
    write_log(response.status_code)
    response.headers["X-Request-Id"] = g.request_id
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(exc: HTTPException):
    response = jsonify(
        {
            "error": exc.name.lower().replace(" ", "_"),
            "status": exc.code,
            "path": request.path,
            "version": APP_VERSION,
        }
    )
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    response = jsonify(
        {
            "error": "internal_server_error",
            "status": 500,
            "path": request.path,
            "version": APP_VERSION,
        }
    )
    response.status_code = 500
    return response


@app.get("/")
def home():
    return jsonify(
        {
            "app": "obsapp-ud12",
            "version": APP_VERSION,
            "status": "running",
            "timestamp": utc_now_iso(),
        }
    ), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok", "version": APP_VERSION, "timestamp": utc_now_iso()}), 200


@app.get("/time")
def current_time():
    return jsonify({"time": utc_now_iso(), "version": APP_VERSION}), 200


@app.post("/echo")
def echo():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "status": 400, "version": APP_VERSION}), 400
    return jsonify({"received": payload, "status": 200, "version": APP_VERSION}), 200


@app.get("/error")
def simulated_error():
    return jsonify({"error": "simulated_error", "status": 500, "version": APP_VERSION}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
