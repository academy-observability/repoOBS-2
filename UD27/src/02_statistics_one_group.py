# UD27 - Script 02
# Obiettivo: calcolare statistiche soltanto su un gruppo preciso di osservazioni.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# CONCETTO GIÀ CONOSCIUTO DA UD26
# Definiamo il gruppo che vogliamo analizzare.
service = "frontend"
endpoint = "/products"

# MODIFICA GUIDATA - TASK 4
# Provare successivamente con:
# service = "backend"
# endpoint = "/api/products"

# Il filtro conserva soltanto le righe che soddisfano entrambe le condizioni.
selected = data[
    (data["service"] == service)
    & (data["endpoint"] == endpoint)
]

# Selezioniamo le durate del solo gruppo scelto.
durations = selected["duration_ms"]

print("Gruppo:", service, endpoint)
print("Count:", durations.count())
print("Minimo:", round(durations.min(), 2), "ms")
print("Massimo:", round(durations.max(), 2), "ms")
print("Media:", round(durations.mean(), 2), "ms")
print("Mediana:", round(durations.median(), 2), "ms")

# LIMITE DEL METODO
# Stiamo descrivendo un solo gruppo.
# Un valore maggiore non significa automaticamente anomalia o incidente.
