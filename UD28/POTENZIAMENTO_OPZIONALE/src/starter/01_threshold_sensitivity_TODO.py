from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"

# CODICE DI SERVIZIO
baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
median = baseline["duration_ms"].median()
mad = (baseline["duration_ms"] - median).abs().median()

# TODO 1: completare i moltiplicatori da confrontare.
multipliers = []

for multiplier in multipliers:
    # TODO 2: calcolare la soglia.
    threshold = 0

    # CODICE DI SERVIZIO: lavoriamo su una copia per non alterare il dataset originale.
    predictions = evaluation[["observation_id", "duration_ms"]].copy()
    predictions["predicted_label"] = "normal"

    # TODO 3: assegnare anomaly quando duration_ms supera la soglia.

    # TODO 4: contare le anomaly prediction.
    anomaly_count = 0

    print(
        "multiplier=", multiplier,
        "threshold=", threshold,
        "predicted_anomalies=", anomaly_count,
    )
