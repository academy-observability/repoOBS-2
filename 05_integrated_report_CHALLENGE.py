# UD27 - Potenziamento 1
# Report statistico multi-gruppo.

from pathlib import Path
import pandas as pd

# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Questo blocco è fornito perché l'obiettivo dell'attività NON è
# imparare a costruire percorsi di file robusti.
#
# Path(__file__) parte dal file Python corrente.
# parents[3] risale dalla cartella:
# POTENZIAMENTO_OPZIONALE/src/starter/
# fino alla cartella UD27.
#
# In questo modo lo script trova il dataset senza dipendere
# dalla directory da cui viene lanciato.
DATASET_PATH = (
    Path(__file__).resolve().parents[3]
    / "datasets"
    / "mini_products_requests.csv"
)

# CODICE DI SERVIZIO
# read_csv() trasforma il CSV in un DataFrame pandas.
# È già stato usato nelle UD precedenti: qui non è il focus.
data = pd.read_csv(DATASET_PATH)


def describe_group(data, service, endpoint):
    """
    CODICE DA COMPRENDERE E COMPLETARE.

    La funzione:
    1. seleziona un solo gruppo service + endpoint;
    2. prende la colonna duration_ms;
    3. restituisce un dizionario con le statistiche.
    """

    selected = data[
        (data["service"] == service)
        & (data["endpoint"] == endpoint)
    ]

    durations = selected["duration_ms"]

    # TODO 1
    # Calcolare la mediana e arrotondare a 2 decimali.
    median_value = None

    # TODO 2
    # Calcolare il p95 e arrotondare a 2 decimali.
    p95_value = None

    return {
        "service": service,
        "endpoint": endpoint,
        "count": durations.count(),
        "min": round(durations.min(), 2),
        "max": round(durations.max(), 2),
        "mean": round(durations.mean(), 2),
        "median": median_value,
        "p95": p95_value,
    }


# TODO 3
# Completare la lista con i quattro gruppi:
# frontend /products
# backend  /api/products
# frontend /products/slow
# backend  /api/products/slow
groups = [
    ("frontend", "/products"),
    ("backend", "/api/products"),
]


results = []

# TODO 4
# Per ogni coppia service/endpoint:
# - chiamare describe_group(...)
# - aggiungere il risultato alla lista results.
for service, endpoint in groups:
    pass


# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Convertiamo la lista di dizionari in DataFrame soltanto per
# ottenere una tabella leggibile.
#
# Non è richiesto costruire manualmente la formattazione.
report = pd.DataFrame(results)

# CODICE DI SERVIZIO
# to_string(index=False) stampa la tabella senza la colonna
# numerica dell'indice pandas, che qui non aggiunge informazione.
print(report.to_string(index=False))
