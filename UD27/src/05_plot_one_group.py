# UD27 - Script 05
# Obiettivo: osservare nel tempo le durate di un singolo gruppo.

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "outputs" / "frontend_products_duration.png"

data = pd.read_csv(DATASET_PATH)

# Scegliamo un gruppo già analizzato con le statistiche.
service = "frontend"
endpoint = "/products"

# MODIFICA GUIDATA - TASK 8
# Per confrontare il backend usare:
# service = "backend"
# endpoint = "/api/products"
# e cambiare OUTPUT_PATH in backend_api_products_duration.png

selected = data[
    (data["service"] == service)
    & (data["endpoint"] == endpoint)
].copy()

# CONCETTO NUOVO
# Convertiamo il testo del timestamp in un tipo temporale riconosciuto da pandas.
# Questo permette di usare correttamente il tempo sull'asse orizzontale.
selected["timestamp_utc"] = pd.to_datetime(selected["timestamp_utc"])

# CODICE DI SERVIZIO
# Ordiniamo le righe per tempo prima di disegnare la linea.
selected = selected.sort_values("timestamp_utc")

# CODICE DI SERVIZIO
# La sintassi di matplotlib non è il nuovo obiettivo della UD.
plt.figure(figsize=(9, 4))
plt.plot(selected["timestamp_utc"], selected["duration_ms"], marker="o")
plt.title(f"{service} {endpoint} - durata nel tempo")
plt.xlabel("timestamp UTC")
plt.ylabel("duration_ms")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
plt.close()

print("Gruppo:", service, endpoint)
print("Righe rappresentate:", len(selected))
print("Grafico creato:", OUTPUT_PATH)

# LIMITE DEL METODO
# Il grafico mostra quando cambiano i valori, ma non definisce da solo
# una baseline e non classifica automaticamente anomalie.
