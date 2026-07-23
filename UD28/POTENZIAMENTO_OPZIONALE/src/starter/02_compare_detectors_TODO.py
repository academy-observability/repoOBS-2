from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
REFERENCE_PATH = ROOT / "datasets" / "products_reference_labels.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "outputs" / "detector_comparison.csv"

# CODICE DI SERVIZIO
baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
reference = pd.read_csv(REFERENCE_PATH)
median = baseline["duration_ms"].median()
mad = (baseline["duration_ms"] - median).abs().median()
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def evaluate_detector(multiplier):
    # TODO: costruire threshold, prediction, confronto e metriche.
    # IMPORTANTE: produrre le prediction prima di usare la reference.
    return {
        "multiplier": multiplier,
        "threshold_ms": 0,
        "TP": 0,
        "FP": 0,
        "FN": 0,
        "TN": 0,
        "precision": 0,
        "recall": 0,
    }


results = []
for multiplier in [2, 3, 4, 5]:
    results.append(evaluate_detector(multiplier))

# CODICE DI SERVIZIO
report = pd.DataFrame(results)
print(report.to_string(index=False))
report.to_csv(OUTPUT_PATH, index=False)
print("\nSalvato in:", OUTPUT_PATH)
