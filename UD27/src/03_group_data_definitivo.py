# UD27 - Script 03
# Obiettivo: capire come groupby suddivide il dataset in gruppi
# e poi applicare automaticamente gli stessi calcoli a ogni gruppo
# service + endpoint.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
# Costruiamo il percorso del dataset in modo indipendente
# dalla cartella da cui viene eseguito lo script.
DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "datasets"
    / "mini_products_requests.csv"
)

# Carichiamo il CSV in un DataFrame pandas.
data = pd.read_csv(DATASET_PATH)


# ============================================================
# 1. OSSERVIAMO IL DATASET COMPLETO
# ============================================================

print("=== DATASET COMPLETO ===")
print(data)


# ============================================================
# 2. CONCETTO NUOVO: GROUPBY
# ============================================================

# In precedenza selezionavamo un singolo gruppo usando
# un filtro esplicito.
#
# Ora groupby separa automaticamente il DataFrame in gruppi.
# La chiave di ogni gruppo è formata dalla combinazione:
#
#     service + endpoint
#
# In questa prima fase NON selezioniamo ancora duration_ms,
# perché vogliamo vedere tutte le righe e tutte le colonne
# appartenenti a ciascun gruppo.
groups = data.groupby(["service", "endpoint"])


# ============================================================
# 3. VEDIAMO CONCRETAMENTE COME È STATO SUDDIVISO IL DATASET
# ============================================================

print("\n=== DATASET SUDDIVISO PER SERVICE + ENDPOINT ===")

# Ogni iterazione restituisce:
#
# - la chiave del gruppo: (service, endpoint)
# - il sotto-DataFrame contenente le righe di quel gruppo
#
# Questo ciclo serve soprattutto a rendere VISIBILE
# ciò che groupby ha organizzato logicamente.
for (service, endpoint), group in groups:
    print(f"\n--- GRUPPO: service={service} | endpoint={endpoint} ---")
    print(group)


# ============================================================
# 4. ORA CI CONCENTRIAMO SULLA COLONNA duration_ms
# ============================================================

# Dopo aver visto i gruppi completi, selezioniamo duration_ms.
# Otteniamo così, per ogni coppia service + endpoint,
# il gruppo dei soli valori di durata su cui calcolare
# le statistiche descrittive.
duration_groups = data.groupby(
    ["service", "endpoint"]
)["duration_ms"]


# ============================================================
# 5. APPLICHIAMO LE STESSE STATISTICHE A OGNI GRUPPO
# ============================================================

print("\n=== COUNT PER GRUPPO ===")
print(duration_groups.count())

print("\n=== MEDIA PER GRUPPO ===")
print(duration_groups.mean().round(2))

print("\n=== MEDIANA PER GRUPPO ===")
print(duration_groups.median().round(2))


# ============================================================
# 6. MODIFICA GUIDATA - TASK 5
# ============================================================

# Dopo aver eseguito e osservato lo script:
#
# sostituire temporaneamente:
#
#     groups = data.groupby(["service", "endpoint"])
#
# con:
#
#     groups = data.groupby(["service"])
#
# e, per mantenere coerente anche la parte statistica,
# sostituire:
#
#     duration_groups = data.groupby(
#         ["service", "endpoint"]
#     )["duration_ms"]
#
# con:
#
#     duration_groups = data.groupby(
#         ["service"]
#     )["duration_ms"]
#
# Osservare:
#
# 1. quanti gruppi rimangono;
# 2. quali righe vengono ora riunite nello stesso gruppo;
# 3. quale informazione perdiamo eliminando endpoint
#    dalla chiave di raggruppamento.


# ============================================================
# LIMITE DEL METODO
# ============================================================

# groupby organizza e riassume i dati.
#
# Le statistiche descrivono il comportamento dei gruppi.
#
# Non decidono però se un gruppo è:
#
# - normale;
# - anomalo;
# - problematico.
#
# Per formulare questo tipo di valutazione sarà necessario
# introdurre un comportamento di riferimento (baseline).
