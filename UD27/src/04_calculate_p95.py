# UD27 - Script 04
# Obiettivo: calcolare il p95 di un gruppo e confrontarlo con mediana e massimo.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# Scegliamo un gruppo già noto.
service = "frontend"
endpoint = "/products"

# MODIFICA GUIDATA - TASK 7
# Provare successivamente con:
# service = "backend"
# endpoint = "/api/products"

selected = data[
    (data["service"] == service)
    & (data["endpoint"] == endpoint)
]

durations = selected["duration_ms"]

# CONCETTO NUOVO
# quantile(0.95) calcola il 95° percentile.
# Il p95 descrive il valore sotto il quale ricade circa il 95% delle osservazioni.
p95 = durations.quantile(0.95)

print("Gruppo:", service, endpoint)
print("Count:", durations.count())
print("Mediana:", round(durations.median(), 2), "ms")
print("P95:", round(p95, 2), "ms")
print("Massimo:", round(durations.max(), 2), "ms")

# LIMITE DEL METODO
# Il p95 è una statistica descrittiva.
# Non è automaticamente una soglia di anomalia e non conferma un incidente.
