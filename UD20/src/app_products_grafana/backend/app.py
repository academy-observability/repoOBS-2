import json
import logging
import os
import random
import sys
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from werkzeug.exceptions import HTTPException

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import extract
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Il backend rappresenta il servizio applicativo interno: espone il catalogo
# prodotti e produce segnali osservabili locali: metriche, log JSON e trace.
SERVICE_NAME = os.getenv("SERVICE_NAME", "products-backend")
APP_VERSION = os.getenv("APP_VERSION", "1.3.0-local-products")
APP_ENV = os.getenv("APP_ENV", "local-compose")
PORT = int(os.getenv("PORT", "8000"))
SLOW_DELAY_SECONDS = float(os.getenv("SLOW_DELAY_SECONDS", "2.5"))
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317")

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(SERVICE_NAME)

resource = Resource.create({"service.name": SERVICE_NAME, "service.version": APP_VERSION, "deployment.environment": APP_ENV})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(SERVICE_NAME)

REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Numero totale di richieste HTTP osservate dall'applicazione",
    ["service", "method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "Durata delle richieste HTTP in secondi",
    ["service", "method", "path"],
)

PRODUCTS = [
    {"id": 1, "name": "notebook", "price": 1200},
    {"id": 2, "name": "monitor", "price": 260},
    {"id": 3, "name": "keyboard", "price": 80},
]

app = Flask(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def current_trace_fields() -> dict:
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if not ctx or not ctx.is_valid:
        return {"trace_id": None, "span_id": None}
    return {"trace_id": format(ctx.trace_id, "032x"), "span_id": format(ctx.span_id, "016x")}


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
        **current_trace_fields(),
        **extra,
    }
    logger.info(json.dumps(record, ensure_ascii=False))


@app.before_request
def before_request() -> None:
    g.start_time = time.perf_counter()
    g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))


@app.after_request
def after_request(response):
    elapsed = time.perf_counter() - g.start_time
    path = request.path if request.path != "/metrics" else "/metrics"
    REQUEST_COUNT.labels(SERVICE_NAME, request.method, path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(SERVICE_NAME, request.method, path).observe(elapsed)
    if request.path != "/metrics":
        write_log(response.status_code)
    response.headers["X-Request-Id"] = g.request_id
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(exc: HTTPException):
    response = jsonify({"error": exc.name.lower().replace(" ", "_"), "status": exc.code, "path": request.path, "request_id": g.request_id})
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    write_log(500, "unhandled_exception", exception_type=type(exc).__name__, exception_message=str(exc))
    response = jsonify({"error": "internal_server_error", "status": 500, "path": request.path, "request_id": g.request_id})
    response.status_code = 500
    return response


def product_response(delay_seconds: float = 0.0):
    parent_context = extract(request.headers)
    with tracer.start_as_current_span("backend.catalog.products", context=parent_context) as span:
        span.set_attribute("app.request_id", g.request_id)
        span.set_attribute("app.products.count", len(PRODUCTS))
        if delay_seconds > 0:
            span.set_attribute("app.simulated_delay_seconds", delay_seconds)
            time.sleep(delay_seconds)
        return jsonify({
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "environment": APP_ENV,
            "items": PRODUCTS,
            "count": len(PRODUCTS),
            "request_id": g.request_id,
            **current_trace_fields(),
        }), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV}), 200


@app.get("/version")
def version():
    return jsonify({"service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV, "timestamp": utc_now_iso()}), 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/api/products")
def products():
    return product_response(random.uniform(0.05, 0.20))


@app.get("/api/products/slow")
def products_slow():
    return product_response(SLOW_DELAY_SECONDS)


@app.get("/api/products/error")
def products_error():
    parent_context = extract(request.headers)
    with tracer.start_as_current_span("backend.catalog.products.error", context=parent_context) as span:
        span.set_attribute("app.request_id", g.request_id)
        span.set_attribute("error", True)
        return jsonify({
            "service": SERVICE_NAME,
            "error": "simulated_product_catalog_error",
            "status": 500,
            "request_id": g.request_id,
            **current_trace_fields(),
        }), 500


@app.get("/work")
def work_compatibility():
    return products()


@app.get("/work-error")
def work_error_compatibility():
    return products_error()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
