# UD26 - Script 03
# Obiettivo: filtrare le righe usando una condizione sulla colonna service.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# CONCETTO NUOVO
# Per ogni riga, questa condizione produce True se service è "frontend"
# e False negli altri casi.
is_selected_service = data["service"] == "frontend"

# Il filtro conserva soltanto le righe associate a True.
selected_rows = data[is_selected_service]

print("Servizio selezionato: frontend")
print("Numero di righe:", len(selected_rows))
print()
print("Prime 5 righe selezionate:")
print(selected_rows.head())

# MODIFICA GUIDATA - TASK 5
# Sostituire "frontend" con "backend" sia nella condizione sia nel messaggio.
# Osservare quali valori cambiano e quali elementi della struttura restano invariati.

# LIMITE DEL METODO
# Il filtro crea un sottoinsieme in memoria.
# Non cancella righe dal CSV originale.
