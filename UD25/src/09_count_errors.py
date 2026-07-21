"""UD25 - Contare righe e status 5xx nel dataset ridotto."""

import csv
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

total_rows = 0
server_errors = 0

with DATASET_PATH.open(newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_rows += 1
        status_code = int(row["status_code"])

        if status_code >= 500:
            server_errors += 1
            print("5xx:", row["service"], row["endpoint"], row["request_id"])

print("Righe totali:", total_rows)
print("Righe con status 5xx:", server_errors)

# TASK 10 è un task di lettura integrata: non richiede modifiche.
# Il partecipante deve spiegare come collaborano open, DictReader, for, int e if.
