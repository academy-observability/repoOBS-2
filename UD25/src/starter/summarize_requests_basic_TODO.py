"""LAB autonomo UD25 - Completare i TODO senza usare pandas."""

import csv
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parents[2] / "datasets" / "mini_products_requests.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "outputs" / "basic_request_summary.txt"

# TODO 1: inizializzare il numero totale di righe e il numero di errori 5xx.
# TODO 2: inizializzare le informazioni della richiesta più lenta.

with DATASET_PATH.open(newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # TODO 3: incrementare il totale delle righe.
        # TODO 4: convertire status_code in int e duration_ms in float.
        # TODO 5: contare gli status 5xx.
        # TODO 6: aggiornare la richiesta più lenta quando necessario.
        pass

# TODO 7: costruire un testo con riepilogo, servizio, endpoint e request_id.
summary = "DA COMPLETARE\n"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(summary, encoding="utf-8")
print(summary)
print("Output scritto in:", OUTPUT_PATH)
