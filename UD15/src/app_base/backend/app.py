import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "local")
PORT = int(os.getenv("PORT", "8000"))

app = Flask(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_log(status_code: int, message: str = "request_completed") -> None:
    latency_ms = round((time.perf_counter() - g.start_time) * 1000, 2)
    record = {
        "timestamp": utc_now_iso(),
        "service": SERVICE_NAME,
        "level": "INFO" if status_code < 400 else "ERROR",
        "message": message,
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status": int(status_code),
        "latency_ms": latency_ms,
        "client_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
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
    response = jsonify({"error": exc.name.lower().replace(" ", "_"), "status": exc.code, "path": request.path})
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    response = jsonify({"error": "internal_server_error", "status": 500, "path": request.path})
    response.status_code = 500
    return response


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV}), 200


@app.get("/version")
def version():
    return jsonify({"service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV, "timestamp": utc_now_iso()}), 200


@app.get("/work")
def work():
    delay = random.uniform(0.05, 0.35)
    time.sleep(delay)
    return jsonify({
        "service": SERVICE_NAME,
        "message": "backend completed work",
        "processing_time_ms": round(delay * 1000, 2),
        "version": APP_VERSION,
        "environment": APP_ENV,
        "request_id": g.request_id,
    }), 200


@app.get("/work-error")
def work_error():
    return jsonify({"service": SERVICE_NAME, "error": "simulated_backend_error", "status": 500, "request_id": g.request_id}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
