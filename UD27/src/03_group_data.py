# UD27 - Script 03
# Obiettivo: usare groupby per ripetere automaticamente lo stesso calcolo
# su tutti i gruppi service + endpoint.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

data = pd.read_csv(DATASET_PATH)

# CONCETTO NUOVO
# In precedenza selezionavamo un gruppo con un filtro esplicito.
# groupby separa automaticamente il DataFrame in gruppi distinti.
# Qui la chiave del gruppo è composta da service + endpoint.
groups = data.groupby(["service", "endpoint"])["duration_ms"]

# MODIFICA GUIDATA - TASK 5
# Sostituire temporaneamente la riga precedente con:
# groups = data.groupby(["service"])["duration_ms"]
# Osservare quanti gruppi rimangono e quale informazione perdiamo.

# Applichiamo le stesse statistiche a ogni gruppo.
print("COUNT PER GRUPPO")
print(groups.count())

print("\nMEDIA PER GRUPPO")
print(groups.mean().round(2))

print("\nMEDIANA PER GRUPPO")
print(groups.median().round(2))

# LIMITE DEL METODO
# groupby organizza e riassume i dati.
# Non decide se un gruppo è normale, anomalo o problematico.
