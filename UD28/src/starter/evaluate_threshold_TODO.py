# UD28 - Laboratorio autonomo
# Completare usando soltanto operazioni già viste nel laboratorio guidato.

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
REFERENCE_PATH = ROOT / "datasets" / "products_reference_labels.csv"

baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
reference = pd.read_csv(REFERENCE_PATH)

# TODO 1: calcolare mediana e MAD
median = None
mad = None

# TODO 2: impostare il moltiplicatore a 3 e calcolare la soglia
multiplier = 3
threshold = None

if median is None or mad is None or threshold is None:
    raise SystemExit("Completare TODO 1 e TODO 2 prima di proseguire.")

# TODO 3: creare predicted_label usando duration_ms e threshold

# TODO 4: associare le prediction alle reference label tramite observation_id

# TODO 5: calcolare TP, FP, FN, TN, precision e recall
