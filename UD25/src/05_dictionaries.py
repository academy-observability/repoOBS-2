"""UD25 - Un dizionario rappresenta una richiesta osservata."""

request = {
    "service": "frontend",
    "endpoint": "/products",
    "status_code": 200,
    "duration_ms": 124.7,
    "request_id": "req-example-001",
    # MODIFICA GUIDATA - TASK 6, PARTE A
    # Togli il carattere # dalla riga seguente.
    # "trace_id": "trace-example-001",
}

print("Dizionario completo:", request)
print("Endpoint:", request["endpoint"])
print("Durata:", request["duration_ms"], "ms")
print("Request ID:", request["request_id"])

# MODIFICA GUIDATA - TASK 6, PARTE B
# Dopo aver aggiunto la chiave al dizionario, togli # dalla riga seguente.
# print("Trace ID:", request["trace_id"])
