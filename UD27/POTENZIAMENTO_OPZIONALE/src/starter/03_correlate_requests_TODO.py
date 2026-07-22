# UD27 - Potenziamento 3
# Analisi di richieste correlate.

from pathlib import Path
import pandas as pd

# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Percorsi già pronti:
# - dataset di input
# - CSV prodotto dallo script
#
# La costruzione dei path non è l'obiettivo del laboratorio.
BASE_UD27 = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    BASE_UD27
    / "datasets"
    / "mini_products_requests.csv"
)

OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "request_correlation_summary.csv"
)

# CODICE DI SERVIZIO
data = pd.read_csv(DATASET_PATH)


request_ids = [
    "req-0067",
    "req-0132",
    "req-0158",
    "req-0005",
]


results = []

for request_id in request_ids:
    # TODO 1
    # Filtrare il DataFrame usando request_id.
    selected = None

    # TODO 2
    # Se non esistono righe:
    # aggiungere comunque a results un dizionario con:
    # request_id
    # rows = 0
    # note = "nessuna osservazione"
    # poi continuare con la prossima iterazione.

    # TODO 3
    # Per le richieste trovate calcolare:
    # - rows
    # - trace_id
    # - services coinvolti
    # - status_codes presenti
    # - min_duration_ms
    # - max_duration_ms
    # - duration_difference_ms
    #
    # Poi aggiungere il dizionario a results.


# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Trasformiamo la lista di risultati in DataFrame per:
# 1. stamparla in forma tabellare;
# 2. salvarla in CSV.
summary = pd.DataFrame(results)

print(summary.to_string(index=False))

# CODICE DI SERVIZIO
# Creiamo la cartella outputs se non esiste.
# exist_ok=True evita errore se esiste già.
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# CODICE DI SERVIZIO
# Salviamo il risultato per poterlo usare come evidenza.
# index=False evita di scrivere nel CSV l'indice tecnico pandas.
summary.to_csv(OUTPUT_PATH, index=False)

print()
print("CSV creato:", OUTPUT_PATH)
