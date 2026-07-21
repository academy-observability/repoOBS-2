# UD26 - Script 02
# Obiettivo: selezionare una singola colonna da un DataFrame.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# CONCETTO NUOVO
# Tra parentesi quadre indichiamo il nome della colonna da selezionare.
# Non stiamo modificando il DataFrame: stiamo osservando una sua parte.
durations = data["duration_ms"]

print("Prime 5 valori della colonna selezionata:")
print(durations.head())

print()
print("Numero di valori presenti nella colonna:")
print(len(durations))

# MODIFICA GUIDATA - TASK 4
# Nel laboratorio sostituiremo "duration_ms" con "status_code"
# per osservare una colonna differente senza cambiare il numero di righe.
