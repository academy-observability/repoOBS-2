"""UD25 - Leggere le prime cinque righe con csv.DictReader."""

import csv
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

with DATASET_PATH.open(newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row_number, row in enumerate(reader, start=1):
        # DictReader restituisce inizialmente testo: convertiamo i numeri.
        status_code = int(row["status_code"])
        duration_ms = float(row["duration_ms"])

        print(
            row_number,
            row["service"],
            row["endpoint"],
            status_code,
            duration_ms,
            row["request_id"],
            # MODIFICA GUIDATA - TASK 9
            # Togli # dalla riga seguente per aggiungere il trace ID all'output.
            # row["trace_id"],
        )

        if row_number == 5:
            break
