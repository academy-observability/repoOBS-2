from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
REFERENCE_PATH = ROOT / "datasets" / "products_reference_labels.csv"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "outputs"

# CODICE DI SERVIZIO
baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
reference = pd.read_csv(REFERENCE_PATH)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# TODO A
# Creare una funzione evaluate_detector(multiplier) e valutare 2, 3, 4, 5.
# Salvare audit_detector_comparison.csv.

# TODO B
# Per multiplier=4 esportare soltanto FP e FN in audit_error_cases.csv.

# TODO C
# Confrontare baseline da 20, 40 e 60 righe.
# Salvare audit_baseline_stability.csv.

# CODICE DI SERVIZIO
print("Completare i tre blocchi TODO e poi compilare templates/conclusioni_challenge.md")
