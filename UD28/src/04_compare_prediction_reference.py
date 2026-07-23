# UD28 - Script 04
# Obiettivo: associare prediction e reference della stessa observation_id.

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS_PATH = ROOT / "outputs" / "predictions.csv"
REFERENCE_PATH = ROOT / "datasets" / "products_reference_labels.csv"
OUTPUT_PATH = ROOT / "outputs" / "comparison.csv"

predictions = pd.read_csv(PREDICTIONS_PATH)
reference = pd.read_csv(REFERENCE_PATH)

# CODICE DI SERVIZIO
# merge associa le righe che hanno la stessa observation_id.
# Non crea nuove observation: mette affiancate informazioni sulla stessa richiesta.
compared = predictions.merge(reference, on="observation_id", how="inner")

# CONCETTO NUOVO
# Classifichiamo ogni confronto come TP, FP, FN o TN.
outcomes = []
for _, row in compared.iterrows():
    predicted = row["predicted_label"]
    expected = row["reference_label"]

    if predicted == "anomaly" and expected == "anomaly":
        outcome = "TP"
    elif predicted == "anomaly" and expected == "normal":
        outcome = "FP"
    elif predicted == "normal" and expected == "anomaly":
        outcome = "FN"
    else:
        outcome = "TN"

    outcomes.append(outcome)

compared["outcome"] = outcomes
compared.to_csv(OUTPUT_PATH, index=False)

print(
    compared[
        [
            "observation_id", "duration_ms", "status_code",
            "predicted_label", "reference_label", "outcome",
            "reference_reason_code", "label_source"
        ]
    ].to_string(index=False)
)
print("\nConfronto salvato in:", OUTPUT_PATH)
