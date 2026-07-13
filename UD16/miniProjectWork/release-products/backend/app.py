import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
APP_VERSION = os.getenv("APP_VERSION", "1.1.0-products")
APP_ENV = os.getenv("APP_ENV", "local")
PORT = int(os.getenv("PORT", "8000"))
SLOW_DELAY_SECONDS = float(os.getenv("SLOW_DELAY_SECONDS", "2.0"))

PRODUCTS = [
    {"id": 1, "name": "notebook", "price": 1200},
    {"id": 2, "name": "monitor", "price": 260},
    {"id": 3, "name": "keyboard", "price": 80},
]

app = Flask(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_log(status_code: int, message: str = "request_completed", **extra) -> None:
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
        **extra,
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
            "request_id": g.request_id,
        }
    )
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    write_log(
        500,
        "unhandled_exception",
        exception_type=type(exc).__name__,
        exception_message=str(exc),
    )
    response = jsonify(
        {
            "error": "internal_server_error",
            "status": 500,
            "path": request.path,
            "request_id": g.request_id,
        }
    )
    response.status_code = 500
    return response


def product_response(delay_seconds: float = 0.0):
    if delay_seconds > 0:
        time.sleep(delay_seconds)
    return jsonify(
        {
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "environment": APP_ENV,
            "items": PRODUCTS,
            "count": len(PRODUCTS),
            "request_id": g.request_id,
        }
    ), 200


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "environment": APP_ENV,
        }
    ), 200


@app.get("/version")
def version():
    return jsonify(
        {
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "environment": APP_ENV,
            "timestamp": utc_now_iso(),
        }
    ), 200


@app.get("/api/products")
def products():
    return product_response(random.uniform(0.05, 0.25))


@app.get("/api/products/slow")
def products_slow():
    return product_response(SLOW_DELAY_SECONDS)


@app.get("/api/products/error")
def products_error():
    return jsonify(
        {
            "service": SERVICE_NAME,
            "error": "simulated_product_catalog_error",
            "status": 500,
            "request_id": g.request_id,
        }
    ), 500


@app.get("/work")
def work_compatibility():
    return products()


@app.get("/work-error")
def work_error_compatibility():
    return products_error()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
