import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone

import requests
from flask import Flask, Response, g, jsonify, render_template_string, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from werkzeug.exceptions import HTTPException

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode

SERVICE_NAME = os.getenv("SERVICE_NAME", "products-frontend")
APP_VERSION = os.getenv("APP_VERSION", "1.7.0-products-tracing")
APP_ENV = os.getenv("APP_ENV", "local-compose")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
PORT = int(os.getenv("PORT", "8080"))
BACKEND_TIMEOUT_SECONDS = float(os.getenv("BACKEND_TIMEOUT_SECONDS", "5.0"))
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317")

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(SERVICE_NAME)

resource = Resource.create(
    {
        "service.name": SERVICE_NAME,
        "service.version": APP_VERSION,
        "deployment.environment": APP_ENV,
    }
)
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True))
)
trace.set_tracer_provider(provider)

app = Flask(__name__)
# Flask crea gli span SERVER. Requests crea gli span CLIENT e propaga
# automaticamente il W3C Trace Context verso il backend.
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

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

HOME_TEMPLATE = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Catalogo prodotti</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 920px; margin: 40px auto; padding: 0 20px; }
    table { border-collapse: collapse; width: 100%; margin-top: 16px; }
    th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
    .meta { background: #f4f4f4; padding: 12px; margin-bottom: 20px; }
    .ok { color: #126b12; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Catalogo prodotti</h1>
  <p class="ok">Frontend e backend comunicano correttamente.</p>
  <div class="meta">
    <div>Frontend: {{ frontend_version }}</div>
    <div>Backend: {{ backend_version }}</div>
    <div>Ambiente: {{ environment }}</div>
    <div>Request ID: {{ request_id }}</div>
    <div>Trace ID: {{ trace_id }}</div>
  </div>
  <table>
    <thead><tr><th>ID</th><th>Prodotto</th><th>Prezzo</th></tr></thead>
    <tbody>
    {% for product in products %}
      <tr><td>{{ product.id }}</td><td>{{ product.name }}</td><td>€ {{ product.price }}</td></tr>
    {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def current_trace_fields() -> dict:
    span_context = trace.get_current_span().get_span_context()
    if not span_context.is_valid:
        return {"trace_id": None, "span_id": None}
    return {
        "trace_id": format(span_context.trace_id, "032x"),
        "span_id": format(span_context.span_id, "016x"),
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
        "backend_url": BACKEND_URL,
        **current_trace_fields(),
        **extra,
    }
    logger.info(json.dumps(record, ensure_ascii=False))


@app.before_request
def before_request() -> None:
    g.start_time = time.perf_counter()
    g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    server_span = trace.get_current_span()
    if server_span.is_recording():
        server_span.set_attribute("app.request_id", g.request_id)


@app.after_request
def after_request(response):
    elapsed = time.perf_counter() - g.start_time
    path = request.path
    REQUEST_COUNT.labels(SERVICE_NAME, request.method, path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(SERVICE_NAME, request.method, path).observe(elapsed)
    if request.path != "/metrics":
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
    current_span = trace.get_current_span()
    if current_span.is_recording():
        current_span.record_exception(exc)
        current_span.set_status(Status(StatusCode.ERROR, str(exc)))
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


def call_backend(path: str, timeout: float = BACKEND_TIMEOUT_SECONDS):
    # RequestsInstrumentor crea lo span CLIENT e inietta traceparent.
    headers = {"X-Request-Id": g.request_id}
    response = requests.get(f"{BACKEND_URL}{path}", headers=headers, timeout=timeout)
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw_body": response.text}
    return response, payload


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
            "backend_url": BACKEND_URL,
            "timestamp": utc_now_iso(),
        }
    ), 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/ready")
def ready():
    try:
        response, payload = call_backend("/health", timeout=3)
    except requests.RequestException as exc:
        return jsonify(
            {
                "status": "not_ready",
                "service": SERVICE_NAME,
                "backend_url": BACKEND_URL,
                "error": type(exc).__name__,
                "request_id": g.request_id,
                **current_trace_fields(),
            }
        ), 503
    if response.status_code != 200:
        return jsonify(
            {
                "status": "not_ready",
                "service": SERVICE_NAME,
                "backend_status": response.status_code,
                "backend_response": payload,
                "request_id": g.request_id,
                **current_trace_fields(),
            }
        ), 503
    return jsonify(
        {
            "status": "ready",
            "service": SERVICE_NAME,
            "backend_status": response.status_code,
            "request_id": g.request_id,
            **current_trace_fields(),
        }
    ), 200


def proxy_products(path: str):
    try:
        response, payload = call_backend(path)
    except requests.RequestException as exc:
        return jsonify(
            {
                "service": SERVICE_NAME,
                "error": "backend_unreachable",
                "detail": type(exc).__name__,
                "request_id": g.request_id,
                **current_trace_fields(),
            }
        ), 502
    return jsonify(
        {
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "environment": APP_ENV,
            "backend_status": response.status_code,
            "backend_response": payload,
            "request_id": g.request_id,
            **current_trace_fields(),
        }
    ), response.status_code


@app.get("/")
def home():
    try:
        response, payload = call_backend("/api/products")
    except requests.RequestException as exc:
        return render_template_string(
            "<h1>Catalogo prodotti non disponibile</h1><p>{{ error }}</p>",
            error=type(exc).__name__,
        ), 502
    if response.status_code != 200:
        return render_template_string(
            "<h1>Catalogo prodotti non disponibile</h1><p>Backend status: {{ status }}</p>",
            status=response.status_code,
        ), 502
    return render_template_string(
        HOME_TEMPLATE,
        products=payload.get("items", []),
        frontend_version=APP_VERSION,
        backend_version=payload.get("version", "unknown"),
        environment=APP_ENV,
        request_id=g.request_id,
        trace_id=current_trace_fields().get("trace_id"),
    ), 200


@app.get("/products")
def products():
    return proxy_products("/api/products")


@app.get("/products/slow")
def products_slow():
    return proxy_products("/api/products/slow")


@app.get("/products/error")
def products_error():
    return proxy_products("/api/products/error")


@app.get("/demo")
def demo_compatibility():
    return products()


@app.get("/demo-error")
def demo_error_compatibility():
    return products_error()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
