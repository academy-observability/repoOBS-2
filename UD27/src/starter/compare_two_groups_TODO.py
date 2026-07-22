# UD27 - Laboratorio autonomo
# Obiettivo: confrontare due gruppi usando soltanto concetti già esercitati.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[2] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# GRUPPO A - già definito
frontend_products = data[
    (data["service"] == "frontend")
    & (data["endpoint"] == "/products")
]

# TODO 1
# Creare il gruppo B selezionando:
# service == "backend"
# endpoint == "/api/products"
backend_products = None

# Selezioniamo le durate del gruppo A.
frontend_durations = frontend_products["duration_ms"]

# TODO 2
# Selezionare la colonna duration_ms del gruppo B.
backend_durations = None

# CONTROLLO DELLO STARTER
# Finché TODO 1 e TODO 2 non sono completati, interrompiamo il programma
# con un messaggio chiaro invece di produrre un risultato parziale ingannevole.
if backend_products is None or backend_durations is None:
    raise SystemExit("Completare TODO 1 e TODO 2 prima di proseguire.")

print("FRONTEND /products")
print("Count:", frontend_durations.count())
print("Minimo:", round(frontend_durations.min(), 2))
print("Massimo:", round(frontend_durations.max(), 2))
print("Media:", round(frontend_durations.mean(), 2))
print("Mediana:", round(frontend_durations.median(), 2))
print("P95:", round(frontend_durations.quantile(0.95), 2))

print("\nBACKEND /api/products")

# TODO 3
# Stampare per backend_durations le stesse sei statistiche usate sopra.
# Non introdurre nuove statistiche.
print("TODO 3 - aggiungere qui le sei stampe per il backend.")
