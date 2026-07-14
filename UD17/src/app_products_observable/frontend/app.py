import json
import logging
import os
import sys
import time
import uuid
from contextlib import nullcontext
from datetime import datetime, timezone

import requests
from flask import Flask, g, jsonify, render_template_string, request
from werkzeug.exceptions import HTTPException

SERVICE_NAME = os.getenv("SERVICE_NAME", "products-frontend")
APP_VERSION = os.getenv("APP_VERSION", "1.2.0-observable-products")
APP_ENV = os.getenv("APP_ENV", "local")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
PORT = int(os.getenv("PORT", "8080"))
BACKEND_TIMEOUT_SECONDS = float(os.getenv("BACKEND_TIMEOUT_SECONDS", "5.0"))
APPINSIGHTS_CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(SERVICE_NAME)

try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace
except Exception:  # pragma: no cover
    configure_azure_monitor = None
    trace = None

if configure_azure_monitor and APPINSIGHTS_CONNECTION_STRING:
    configure_azure_monitor(connection_string=APPINSIGHTS_CONNECTION_STRING)

tracer = trace.get_tracer(SERVICE_NAME) if trace else None
app = Flask(__name__)

HOME_TEMPLATE = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Catalogo prodotti</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
    .meta { background: #f4f4f4; padding: 12px; margin-bottom: 20px; }
  </style>
</head>
<body>
  <h1>Catalogo prodotti</h1>
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


def span_ctx(name: str):
    return tracer.start_as_current_span(name) if tracer else nullcontext()


def trace_fields() -> dict:
    if not trace:
        return {"trace_id": None, "span_id": None}
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
        "backend_url": BACKEND_URL,
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
    response = jsonify({"error": exc.name.lower().replace(" ", "_"), "status": exc.code, "path": request.path, "request_id": g.request_id})
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def handle_generic_exception(exc: Exception):
    write_log(500, "unhandled_exception", exception_type=type(exc).__name__, exception_message=str(exc))
    response = jsonify({"error": "internal_server_error", "status": 500, "path": request.path, "request_id": g.request_id})
    response.status_code = 500
    return response


def call_backend(path: str, timeout: float = BACKEND_TIMEOUT_SECONDS):
    with span_ctx(f"frontend.call_backend {path}"):
        response = requests.get(f"{BACKEND_URL}{path}", headers={"X-Request-Id": g.request_id}, timeout=timeout)
        try:
            payload = response.json()
        except ValueError:
            payload = {"raw_body": response.text}
        return response, payload


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV}), 200


@app.get("/version")
def version():
    return jsonify({"service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV, "backend_url": BACKEND_URL, "timestamp": utc_now_iso()}), 200


@app.get("/ready")
def ready():
    try:
        response, payload = call_backend("/health", timeout=3)
    except requests.RequestException as exc:
        return jsonify({"status": "not_ready", "service": SERVICE_NAME, "backend_url": BACKEND_URL, "error": type(exc).__name__, "request_id": g.request_id}), 503
    if response.status_code != 200:
        return jsonify({"status": "not_ready", "service": SERVICE_NAME, "backend_status": response.status_code, "backend_response": payload, "backend_url": BACKEND_URL, "request_id": g.request_id}), 503
    return jsonify({"status": "ready", "service": SERVICE_NAME, "backend_status": response.status_code, "backend_url": BACKEND_URL, "request_id": g.request_id}), 200


def proxy_products(path: str):
    try:
        response, payload = call_backend(path)
    except requests.RequestException as exc:
        return jsonify({"service": SERVICE_NAME, "error": "backend_unreachable", "detail": type(exc).__name__, "backend_url": BACKEND_URL, "request_id": g.request_id}), 502
    return jsonify({"service": SERVICE_NAME, "version": APP_VERSION, "environment": APP_ENV, "backend_url": BACKEND_URL, "backend_status": response.status_code, "backend_response": payload, "request_id": g.request_id, **trace_fields()}), response.status_code


@app.get("/")
def home():
    try:
        response, payload = call_backend("/api/products")
    except requests.RequestException as exc:
        return render_template_string("<h1>Catalogo prodotti non disponibile</h1><p>{{ error }}</p>", error=type(exc).__name__), 502
    if response.status_code != 200:
        return render_template_string("<h1>Catalogo prodotti non disponibile</h1><p>Backend status: {{ status }}</p>", status=response.status_code), 502
    return render_template_string(
        HOME_TEMPLATE,
        products=payload.get("items", []),
        frontend_version=APP_VERSION,
        backend_version=payload.get("version", "unknown"),
        environment=APP_ENV,
        request_id=g.request_id,
        trace_id=trace_fields().get("trace_id"),
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
