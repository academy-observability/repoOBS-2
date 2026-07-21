# UD26 - Script 01
# Obiettivo: caricare l'intero CSV in un DataFrame e osservare la sua struttura.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
# __file__ indica il file Python in esecuzione.
# parents[1] risale dalla cartella src alla cartella UD26.
# Costruiamo così il percorso del CSV senza dipendere dalla cartella corrente del terminale.
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

# CONCETTO NUOVO
# read_csv legge il file e costruisce in memoria un DataFrame.
# Un DataFrame è una tabella composta da righe e colonne.
data = pd.read_csv(DATASET_PATH)

print("Prime 5 righe del DataFrame:")
print(data.head())

print()
print("Dimensione del DataFrame (righe, colonne):")
print(data.shape)

print()
print("Nomi delle colonne:")
print(list(data.columns))

print()
print("Tipi riconosciuti da pandas:")
print(data.dtypes)

# LIMITE DEL METODO
# In questo script osserviamo soltanto la struttura.
# Non stiamo ancora calcolando statistiche e non stiamo cercando anomalie.
