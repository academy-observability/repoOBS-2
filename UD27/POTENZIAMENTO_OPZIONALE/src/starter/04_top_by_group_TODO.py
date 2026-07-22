# UD27 - Potenziamento 4
# Top osservazioni per gruppo.

from pathlib import Path
import pandas as pd

# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Percorsi già pronti per mantenere il focus sull'analisi.
BASE_UD27 = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    BASE_UD27
    / "datasets"
    / "mini_products_requests.csv"
)

OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "top_observations_by_group.csv"
)

data = pd.read_csv(DATASET_PATH)


def take_top_rows(selected, top_n):
    """
    CODICE DI SERVIZIO.

    sort_values(..., ascending=False)
    ordina duration_ms dal valore più alto al più basso.

    head(top_n)
    prende soltanto le prime N righe.

    Questa sintassi è fornita perché il focus è applicare
    correttamente l'operazione a più gruppi.
    """
    return (
        selected
        .sort_values("duration_ms", ascending=False)
        .head(top_n)
        .copy()
    )


# TODO 1
# Completare i due gruppi principali.
groups = [
    # ("frontend", "/products"),
    # ("backend", "/api/products"),
]

top_n = 3

all_top_rows = []

for service, endpoint in groups:
    # TODO 2
    # Filtrare data usando service + endpoint.
    selected = None

    # CODICE DI SERVIZIO
    # La funzione fornita ordina e prende le prime top_n righe.
    top_rows = take_top_rows(selected, top_n)

    # TODO 3
    # Creare la colonna rank:
    # [1, 2, ..., numero di righe ottenute]

    # TODO 4
    # Aggiungere top_rows alla lista all_top_rows.


# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# concat unisce verticalmente i DataFrame raccolti nella lista.
# ignore_index=True ricrea un indice progressivo pulito.
final_report = pd.concat(
    all_top_rows,
    ignore_index=True,
)

columns_to_show = [
    "service",
    "endpoint",
    "rank",
    "timestamp_utc",
    "duration_ms",
    "request_id",
    "trace_id",
]

final_report = final_report[columns_to_show]

print(final_report.to_string(index=False))

# CODICE DI SERVIZIO
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# CODICE DI SERVIZIO
final_report.to_csv(OUTPUT_PATH, index=False)

print()
print("CSV creato:", OUTPUT_PATH)
