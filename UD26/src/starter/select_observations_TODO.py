# UD26 - Laboratorio autonomo
# Completare solo i blocchi TODO usando operazioni già viste nel laboratorio guidato.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[2] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# TODO 1
# Creare un filtro che selezioni le righe con service == "frontend".
frontend_rows = None

# TODO 2
# Creare un filtro che selezioni le righe con service == "backend".
backend_rows = None

# TODO 3
# Creare un filtro che selezioni le righe con status_code >= 500.
server_error_rows = None

# TODO 4
# Stampare per ciascun sottoinsieme:
# - numero di righe con len(...)
# - prime due righe con .head(2)

print("Completa i TODO e poi riesegui lo script.")
