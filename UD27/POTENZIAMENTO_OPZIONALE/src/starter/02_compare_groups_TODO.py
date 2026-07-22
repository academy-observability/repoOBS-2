# UD27 - Potenziamento 2
# Confronto tra due gruppi.

from pathlib import Path
import pandas as pd

# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# Il percorso del dataset è già costruito per evitare che
# l'attività diventi un esercizio sulla gestione dei path.
DATASET_PATH = (
    Path(__file__).resolve().parents[3]
    / "datasets"
    / "mini_products_requests.csv"
)

# CODICE DI SERVIZIO
# Carichiamo il CSV nel DataFrame.
data = pd.read_csv(DATASET_PATH)


def select_group(data, service, endpoint):
    """
    CODICE DI SERVIZIO.

    Questa funzione è fornita perché il filtro pandas è già stato
    studiato in UD26. Qui vogliamo concentrarci sulla costruzione
    del confronto, non riscrivere ogni volta lo stesso filtro.
    """
    return data[
        (data["service"] == service)
        & (data["endpoint"] == endpoint)
    ]


def compare_groups(
    data,
    service_a,
    endpoint_a,
    service_b,
    endpoint_b,
):
    """
    TODO PRINCIPALE.

    Costruire il confronto tra i due gruppi.

    Suggerimento di sequenza:

    1. selezionare gruppo A e gruppo B con select_group();
    2. prendere duration_ms;
    3. calcolare mean, median e p95;
    4. calcolare A - B per ogni statistica;
    5. restituire un dizionario.
    """

    # TODO
    pass


comparison = compare_groups(
    data,
    "frontend",
    "/products",
    "backend",
    "/api/products",
)


# ============================================================
# CODICE DI SERVIZIO
# ============================================================
# La stampa è già predisposta perché l'obiettivo non è
# esercitarsi sulla formattazione dell'output.
#
# Usiamo un ciclo per mostrare ordinatamente tutte le coppie
# chiave/valore restituite dalla funzione.
print("=== CONFRONTO GRUPPI ===")
for key, value in comparison.items():
    print(f"{key}: {value}")
