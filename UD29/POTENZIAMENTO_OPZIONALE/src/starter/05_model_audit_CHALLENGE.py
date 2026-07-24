from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[2]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_PATH = ROOT / "datasets" / "ml_test_features.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"
OUTPUT_DIR = ROOT / "POTENZIAMENTO_OPZIONALE" / "outputs"
FEATURES = ["duration_ms", "status_code"]
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)
reference = pd.read_csv(REFERENCE_PATH)

# TODO 1 — costruire e addestrare lo stesso Decision Tree della UD29.
model = None

if model is None:
    raise SystemExit("Completare TODO 1: model + fit")

# TODO 2 — produrre le prediction sul test.
predictions = None

if predictions is None:
    raise SystemExit("Completare TODO 2: predictions")

# CODICE DI SERVIZIO
predicted = test.copy()
predicted["prediction"] = predictions
evaluation = predicted.merge(reference, on="observation_id", how="inner")

# TODO 3 — calcolare TP, FP, FN, TN, precision e recall.
tp = fp = fn = tn = None
precision = recall = None

if None in (tp, fp, fn, tn, precision, recall):
    raise SystemExit("Completare TODO 3: metriche")

# TODO 4 — selezionare i casi errati.
errors = None
if errors is None:
    raise SystemExit("Completare TODO 4: errors")

# TODO 5 — costruire probe con duration_ms=170 e status 200,300,404,500.
probe = None
if probe is None:
    raise SystemExit("Completare TODO 5: probe")
probe["prediction"] = model.predict(probe[FEATURES])

# CODICE DI SERVIZIO — esportazioni
(OUTPUT_DIR / "model_rules.txt").write_text(
    export_text(model, feature_names=FEATURES), encoding="utf-8"
)

pd.DataFrame([{
    "TP": tp, "FP": fp, "FN": fn, "TN": tn,
    "precision": precision, "recall": recall,
}]).to_csv(OUTPUT_DIR / "evaluation_summary.csv", index=False)

errors.to_csv(OUTPUT_DIR / "misclassified_cases.csv", index=False)
probe.to_csv(OUTPUT_DIR / "synthetic_probe.csv", index=False)

print("Audit completato. Output in:", OUTPUT_DIR)
