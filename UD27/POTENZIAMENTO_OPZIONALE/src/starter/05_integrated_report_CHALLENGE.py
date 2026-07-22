# UD27 - Challenge finale
# Report integrato di Observability descrittiva.

from pathlib import Path
import pandas as pd

# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Tutti i percorsi sono già forniti.
# Motivo: il focus della challenge è progettare l'analisi,
# non la gestione del filesystem.
BASE_UD27 = Path(__file__).resolve().parents[3]
POT_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_UD27
    / "datasets"
    / "mini_products_requests.csv"
)

GROUP_SUMMARY_PATH = (
    POT_DIR
    / "outputs"
    / "group_summary.csv"
)

TOP_REQUESTS_PATH = (
    POT_DIR
    / "outputs"
    / "top_requests.csv"
)

# CODICE DI SERVIZIO
data = pd.read_csv(DATASET_PATH)

# CODICE DI SERVIZIO
# Creiamo preventivamente outputs/ per evitare errori
# durante il salvataggio.
GROUP_SUMMARY_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


def export_csv(dataframe, path):
    """
    CODICE DI SERVIZIO.

    Centralizziamo il salvataggio CSV in una funzione per non
    ripetere dettagli tecnici non centrali nella challenge.
    """
    dataframe.to_csv(path, index=False)
    print("CSV creato:", path)


def take_top_rows(selected, top_n):
    """
    CODICE DI SERVIZIO.

    Ordina per duration_ms decrescente e prende le prime N righe.
    La sintassi pandas è fornita: il partecipante deve decidere
    quando e su quali gruppi applicarla.
    """
    return (
        selected
        .sort_values("duration_ms", ascending=False)
        .head(top_n)
        .copy()
    )


def describe_group(data, service, endpoint):
    """
    TODO 1

    Restituire un dizionario con:

    service
    endpoint
    count
    mean
    median
    p95
    max
    """
    pass


# TODO 2
# Definire i due gruppi principali.
groups = []


# TODO 3
# Costruire group_results usando un ciclo e describe_group().
group_results = []


# CODICE DI SERVIZIO
# Convertiamo i risultati in DataFrame per stampa ed export.
group_summary = pd.DataFrame(group_results)

print("=== GROUP SUMMARY ===")
print(group_summary.to_string(index=False))

# CODICE DI SERVIZIO
export_csv(
    group_summary,
    GROUP_SUMMARY_PATH,
)


# TODO 4
# Usando le righe di group_summary:
# calcolare frontend - backend per:
# mean
# median
# p95
#
# Stampare le tre differenze.


# TODO 5
# Per ogni gruppo:
# - filtrare il DataFrame;
# - ottenere top 3 con take_top_rows();
# - aggiungere rank 1..N;
# - aggiungere il DataFrame alla lista top_results.
top_results = []


# CODICE DI SERVIZIO
# Uniamo i DataFrame delle top richieste.
top_requests = pd.concat(
    top_results,
    ignore_index=True,
)

# TODO 6
# Conservare soltanto:
# service
# endpoint
# rank
# timestamp_utc
# status_code
# duration_ms
# request_id
# trace_id


print()
print("=== TOP REQUESTS ===")
print(top_requests.to_string(index=False))

# CODICE DI SERVIZIO
export_csv(
    top_requests,
    TOP_REQUESTS_PATH,
)
