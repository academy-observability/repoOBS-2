# UD28 - Script 06
# Obiettivo: osservare come una soglia diversa cambia gli errori del detector.

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
REFERENCE_PATH = ROOT / "datasets" / "products_reference_labels.csv"

baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)
reference = pd.read_csv(REFERENCE_PATH)

median = baseline["duration_ms"].median()
mad = (baseline["duration_ms"] - median).abs().median()

# CODICE DI SERVIZIO
# Questa funzione ripete lo stesso confronto per un moltiplicatore scelto.
def evaluate_multiplier(multiplier):
    threshold = median + multiplier * mad

    predictions = evaluation[["observation_id", "duration_ms"]].copy()
    predictions["predicted_label"] = "normal"
    predictions.loc[predictions["duration_ms"] > threshold, "predicted_label"] = "anomaly"

    compared = predictions.merge(reference, on="observation_id", how="inner")

    tp = ((compared["predicted_label"] == "anomaly") & (compared["reference_label"] == "anomaly")).sum()
    fp = ((compared["predicted_label"] == "anomaly") & (compared["reference_label"] == "normal")).sum()
    fn = ((compared["predicted_label"] == "normal") & (compared["reference_label"] == "anomaly")).sum()
    tn = ((compared["predicted_label"] == "normal") & (compared["reference_label"] == "normal")).sum()

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    return threshold, tp, fp, fn, tn, precision, recall

for multiplier in [4, 3]:
    threshold, tp, fp, fn, tn, precision, recall = evaluate_multiplier(multiplier)
    print("\nMoltiplicatore:", multiplier)
    print("Soglia:", threshold, "ms")
    print("TP:", tp, "FP:", fp, "FN:", fn, "TN:", tn)
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 2))

# LIMITE DEL METODO
# Una soglia più bassa può aumentare il recall ma anche i falsi positivi.
