# UD28 - Script 03
# Obiettivo: leggere la ground truth e comprenderne provenienza e motivazione.

from pathlib import Path
import pandas as pd

REFERENCE_PATH = Path(__file__).resolve().parents[1] / "datasets" / "products_reference_labels.csv"

reference = pd.read_csv(REFERENCE_PATH)

print("Colonne del reference file:")
for column in reference.columns:
    print("-", column)

print("\nReference labels:")
print(
    reference[
        ["observation_id", "reference_label", "reference_reason_code", "label_source"]
    ].to_string(index=False)
)

print("\nDettaglio delle anomaly di riferimento:")
anomalies = reference[reference["reference_label"] == "anomaly"]
for _, row in anomalies.iterrows():
    print("\n", row["observation_id"])
    print("  motivo:", row["reference_reason"])
    print("  fonte:", row["label_source"])

# IMPORTANTE
# Questo file non contiene nuove observation.
# Le observation_id eval-* sono le stesse del file evaluation.
