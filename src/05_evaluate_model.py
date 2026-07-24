from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS_PATH = ROOT / "outputs" / "ml_test_predictions.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"

# UD29 - Script 04
# Obiettivo: valutare prediction già prodotte confrontandole con la reference separata.

if not PREDICTIONS_PATH.exists():
    raise SystemExit(
        "Manca outputs/ml_test_predictions.csv. "
        "Eseguire prima: python src/04_predict_test.py"
    )

predictions = pd.read_csv(PREDICTIONS_PATH)
reference = pd.read_csv(REFERENCE_PATH)

# CODICE DI SERVIZIO
# Il merge collega prediction e reference della STESSA osservazione tramite observation_id.
# Non crea nuove osservazioni e non serve a fare predict.
evaluation = predictions.merge(reference, on="observation_id", how="inner")

if len(evaluation) != len(predictions) or len(evaluation) != len(reference):
    raise SystemExit("Errore: prediction e reference non hanno corrispondenza 1:1.")

# CONCETTO GIÀ NOTO DA UD28
# Confrontiamo prediction e reference_label.
tp = ((evaluation["prediction"] == "anomaly") & (evaluation["reference_label"] == "anomaly")).sum()
fp = ((evaluation["prediction"] == "anomaly") & (evaluation["reference_label"] == "normal")).sum()
fn = ((evaluation["prediction"] == "normal") & (evaluation["reference_label"] == "anomaly")).sum()
tn = ((evaluation["prediction"] == "normal") & (evaluation["reference_label"] == "normal")).sum()

precision = tp / (tp + fp) if (tp + fp) else 0.0
recall = tp / (tp + fn) if (tp + fn) else 0.0

print("TP:", tp)
print("FP:", fp)
print("FN:", fn)
print("TN:", tn)
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))

# CODICE DI SERVIZIO
# Mostriamo i falsi negativi per capire il limite delle feature selezionate.
false_negatives = evaluation[
    (evaluation["reference_label"] == "anomaly")
    & (evaluation["prediction"] == "normal")
][[
    "observation_id", "duration_ms", "status_code", "prediction",
    "reference_label", "reference_reason", "label_source"
]]

print("\nFalsi negativi:")
print(false_negatives.to_string(index=False))

# LIMITE DEL METODO
# Il modello ha visto solo duration_ms e status_code.
# Alcune label possono dipendere da evidenze non presenti in queste due feature.
