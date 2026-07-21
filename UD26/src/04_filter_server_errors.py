# UD26 - Script 04
# Obiettivo: riutilizzare la stessa logica di filtro su una colonna numerica.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# CONCETTO CONSOLIDATO
# La condizione vale True quando lo status HTTP è 500 o superiore.
is_server_error = data["status_code"] >= 500

server_errors = data[is_server_error]

print("Numero di osservazioni selezionate:", len(server_errors))
print()
print("Osservazioni selezionate:")
print(server_errors)

# MODIFICA GUIDATA - TASK 6
# Sostituire >= 500 con == 200.
# Prima di eseguire, prevedere se il numero di righe aumenterà o diminuirà.

# LIMITE DEL METODO
# Status 5xx non significa automaticamente root cause o incidente confermato.
# In questa UD stiamo soltanto selezionando righe che soddisfano una condizione.
