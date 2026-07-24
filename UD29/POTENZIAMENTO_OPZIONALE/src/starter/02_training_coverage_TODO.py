from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[2]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_PATH = ROOT / "datasets" / "ml_test_features.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"

training_data = pd.read_csv(TRAIN_PATH)
test_features = pd.read_csv(TEST_PATH)
reference = pd.read_csv(REFERENCE_PATH)
test_eval = test_features.merge(reference, on="observation_id", how="inner")
FEATURES = ["duration_ms", "status_code"]

# TODO 1
# Creare una copia del training che escluda status_code == 500.
training_without_500 = None

if training_without_500 is None:
    raise SystemExit("Completare TODO 1: training_without_500")


def run_experiment(name, train_df):
    """CODICE DI SERVIZIO: stesso modello, stesso test, training differente."""
    model = DecisionTreeClassifier(max_depth=2, random_state=42)
    model.fit(train_df[FEATURES], train_df["reference_label"])
    pred = model.predict(test_eval[FEATURES])
    y = test_eval["reference_label"]

    tp = ((pred == "anomaly") & (y == "anomaly")).sum()
    fp = ((pred == "anomaly") & (y == "normal")).sum()
    fn = ((pred == "normal") & (y == "anomaly")).sum()
    tn = ((pred == "normal") & (y == "normal")).sum()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    print("\n===", name, "===")
    print("Righe training:", len(train_df))
    print(export_text(model, feature_names=FEATURES))
    print("TP", tp, "FP", fp, "FN", fn, "TN", tn)
    print("Precision", round(precision, 2), "Recall", round(recall, 2))

    errors = test_eval.copy()
    errors["prediction"] = pred
    errors = errors[errors["prediction"] != errors["reference_label"]]
    print("Errori:")
    print(errors[["observation_id", "duration_ms", "status_code", "reference_label", "prediction"]].to_string(index=False))

# TODO 2
# Eseguire l'esperimento sul training completo e sul training_without_500.
