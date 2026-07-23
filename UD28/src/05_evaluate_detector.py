# UD28 - Script 05
# Obiettivo: calcolare TP, FP, FN, TN, precision e recall.

from pathlib import Path
import pandas as pd

COMPARISON_PATH = Path(__file__).resolve().parents[1] / "outputs" / "comparison.csv"

compared = pd.read_csv(COMPARISON_PATH)

# Contiamo quante righe appartengono a ogni risultato.
tp = (compared["outcome"] == "TP").sum()
fp = (compared["outcome"] == "FP").sum()
fn = (compared["outcome"] == "FN").sum()
tn = (compared["outcome"] == "TN").sum()

# CONCETTO NUOVO
# Precision: tra i casi segnalati, quanti erano anomaly di riferimento?
precision = tp / (tp + fp) if (tp + fp) else 0

# Recall: tra tutte le anomaly di riferimento, quante sono state trovate?
recall = tp / (tp + fn) if (tp + fn) else 0

print("TP:", tp)
print("FP:", fp)
print("FN:", fn)
print("TN:", tn)
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))

print("\nFalso negativo da spiegare:")
print(
    compared[compared["outcome"] == "FN"]
    [["observation_id", "duration_ms", "status_code", "reference_reason", "label_source"]]
    .to_string(index=False)
)
