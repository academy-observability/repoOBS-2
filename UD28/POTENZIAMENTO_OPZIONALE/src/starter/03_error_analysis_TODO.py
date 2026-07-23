from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
REFERENCE_PATH = ROOT / "datasets" / "products_reference_labels.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "outputs" / "error_cases.csv"

# CODICE DI SERVIZIO
baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
reference = pd.read_csv(REFERENCE_PATH)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

median = baseline["duration_ms"].median()
mad = (baseline["duration_ms"] - median).abs().median()
multiplier = 4
threshold = median + multiplier * mad

# TODO 1: creare predicted_label usando SOLO duration_ms.

# CODICE DI SERVIZIO
compared = evaluation.merge(reference, on="observation_id", how="inner")

# TODO 2: classificare ogni riga come TP, FP, FN o TN.
# Suggerimento: costruire una lista outcomes.

# TODO 3: filtrare soltanto FP e FN.
errors = compared.iloc[0:0].copy()

columns = [
    "observation_id", "duration_ms", "status_code",
    "predicted_label", "reference_label", "outcome",
    "reference_reason_code", "reference_reason", "label_source",
]

# CODICE DI SERVIZIO
errors = errors[columns]
print(errors.to_string(index=False))
errors.to_csv(OUTPUT_PATH, index=False)
print("\nSalvato in:", OUTPUT_PATH)
