"""UD25 - Più richieste come lista di dizionari."""

requests = [
    {
        "service": "frontend",
        "endpoint": "/products",
        "status_code": 200,
        "duration_ms": 124.7,
    },
    {
        "service": "backend",
        "endpoint": "/api/products",
        "status_code": 200,
        "duration_ms": 78.2,
    },
    {
        "service": "backend",
        "endpoint": "/api/products",
        "status_code": 500,
        "duration_ms": 210.5,
    },
]

# PRIMA MODIFICA - lo script stampa tutte le richieste.
for request in requests:
    print(
        request["service"],
        request["endpoint"],
        request["status_code"],
        request["duration_ms"],
    )

# MODIFICA GUIDATA - TASK 7
# Nel laboratorio sostituiremo il ciclo precedente con un ciclo che contiene:
# if request["status_code"] >= 500:
# e indenteremo la print dentro l'if.
