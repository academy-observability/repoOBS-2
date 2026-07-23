from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "outputs" / "baseline_stability.csv"

# CODICE DI SERVIZIO
baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

multiplier = 4
sizes = [20, 40, 60]
results = []

for size in sizes:
    # TODO 1: selezionare le prime 'size' righe della baseline.
    selected = None

    # TODO 2: calcolare median, MAD e threshold.
    median = 0
    mad = 0
    threshold = 0

    # TODO 3: contare quante evaluation observation superano la soglia.
    predicted_anomalies = 0

    results.append({
        "baseline_size": size,
        "median_ms": median,
        "mad_ms": mad,
        "threshold_ms": threshold,
        "predicted_anomalies": predicted_anomalies,
    })

# CODICE DI SERVIZIO
report = pd.DataFrame(results)
print(report.to_string(index=False))
report.to_csv(OUTPUT_PATH, index=False)
print("\nSalvato in:", OUTPUT_PATH)
