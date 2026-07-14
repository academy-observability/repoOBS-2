import json
import logging
import os
import random
import sys
import time
import uuid
from contextlib import nullcontext
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

# Configurazione base del servizio: gli stessi nomi vengono usati nei log,
# nelle query KQL e nella correlazione tra frontend e backend.
SERVICE_NAME = os.getenv("SERVICE_NAME", "products-backend")
APP_VERSION = os.getenv("APP_VERSION", "1.2.0-observable-products")
APP_ENV = os.getenv("APP_ENV", "local")
PORT = int(os.getenv("PORT", "8000"))
SLOW_DELAY_SECONDS = float(os.getenv("SLOW_DELAY_SECONDS", "2.0"))
APPINSIGHTS_CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(SERVICE_NAME)

# Azure Monitor OpenTelemetry è facoltativo in locale: se la connection string
# non è presente, l'app continua a funzionare e produce comunque log JSON su stdout.
try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace
except Exception:  # pragma: no cover - fallback didattico se i pacchetti non sono installati
    configure_azure_monitor = None
    trace = None

if configure_azure_monitor and APPINSIGHTS_CONNECTION_STRING:
    configure_azure_monitor(connection_string=APPINSIGHTS_CONNECTION_STRING)

tracer = trace.get_tracer(SERVICE_NAME) if trace else None

PRODUCTS = [
    {"id": 1, "name": "notebook", "price": 1200},
    {"id": 2, "name": "monitor", "price": 260},
    {"id": 3, "name": "keyboard", "price": 80},
]

app = Flask(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def span_ctx(name: str):
    return tracer.start_as_current_span(name) if tracer else nullcontext()


def trace_fields() -> dict:
    if not trace:
        return {"trace_id": None, "span_id": None}
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if not ctx or not ctx.is_valid:
        return {"trace_id": None, "span_id": None}
    return {
        "trace_id": format(ctx.trace_id, "032x"),
        "span_id": format(ctx.span_id, "016x"),
    }


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
        **trace_fields(),
        **extra,
    }
    logger.info(json.dumps(record, ensure_ascii=False))


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
    response = jsonify({
        "error": exc.name.lower().replace(" ", "_"),
        "status": exc.code,
        "path": request.path,
        "request_id": g.request_id,
    })
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    write_log(500, "unhandled_exception", exception_type=type(exc).__name__, exception_message=str(exc))
    response = jsonify({
        "error": "internal_server_error",
        "status": 500,
        "path": request.path,
        "request_id": g.request_id,
    })
    response.status_code = 500
    return response


def product_response(delay_seconds: float = 0.0):
    with span_ctx("backend.catalog.products"):
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        return jsonify({
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "environment": APP_ENV,
            "items": PRODUCTS,
            "count": len(PRODUCTS),
            "request_id": g.request_id,
            **trace_fields(),
        }), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV}), 200


@app.get("/version")
def version():
    return jsonify({"service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV, "timestamp": utc_now_iso()}), 200


@app.get("/api/products")
def products():
    return product_response(random.uniform(0.05, 0.25))


@app.get("/api/products/slow")
def products_slow():
    return product_response(SLOW_DELAY_SECONDS)


@app.get("/api/products/error")
def products_error():
    return jsonify({
        "service": SERVICE_NAME,
        "error": "simulated_product_catalog_error",
        "status": 500,
        "request_id": g.request_id,
        **trace_fields(),
    }), 500


# Compatibilità con i laboratori precedenti: non è più il percorso principale.
@app.get("/work")
def work_compatibility():
    return products()


@app.get("/work-error")
def work_error_compatibility():
    return products_error()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
