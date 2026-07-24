from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[2]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_FEATURES_PATH = ROOT / "datasets" / "ml_test_features.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"

# UD29 - Laboratorio autonomo
# Obiettivo: confrontare lo stesso algoritmo con una o due feature.

training_data = pd.read_csv(TRAIN_PATH)
test_features = pd.read_csv(TEST_FEATURES_PATH)
reference = pd.read_csv(REFERENCE_PATH)

# CODICE DI SERVIZIO
# La reference viene unita solo per la valutazione finale.
test_evaluation = test_features.merge(reference, on="observation_id", how="inner")

# TODO 1
FEATURES_A = None

# TODO 2
FEATURES_B = None


def evaluate(feature_columns):
    """CODICE DI SERVIZIO: addestra, predice e poi valuta lo stesso Decision Tree."""
    X_train = training_data[feature_columns]
    y_train = training_data["reference_label"]
    X_test = test_evaluation[feature_columns]
    y_test = test_evaluation["reference_label"]

    model = DecisionTreeClassifier(max_depth=2, random_state=42)
    model.fit(X_train, y_train)

    # predict riceve SOLO X_test: la reference_label non è una feature.
    predictions = model.predict(X_test)

    tp = ((predictions == "anomaly") & (y_test == "anomaly")).sum()
    fp = ((predictions == "anomaly") & (y_test == "normal")).sum()
    fn = ((predictions == "normal") & (y_test == "anomaly")).sum()
    tn = ((predictions == "normal") & (y_test == "normal")).sum()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return tp, fp, fn, tn, precision, recall


if FEATURES_A is None or FEATURES_B is None:
    raise SystemExit("Completare TODO 1 e TODO 2 prima di eseguire il confronto.")

# TODO 3
# Eseguire evaluate(FEATURES_A) ed evaluate(FEATURES_B)
# e stampare i risultati in modo confrontabile.
