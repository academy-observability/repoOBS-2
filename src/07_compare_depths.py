from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_FEATURES_PATH = ROOT / "datasets" / "ml_test_features.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"

# UD29 - Script 06
# Obiettivo: osservare che un modello più complesso non è automaticamente migliore.

training_data = pd.read_csv(TRAIN_PATH)
test_features = pd.read_csv(TEST_FEATURES_PATH)
reference = pd.read_csv(REFERENCE_PATH)

# CODICE DI SERVIZIO
# Colleghiamo le reference alle test observation solo per poter misurare le prestazioni.
# Le label non vengono incluse in X_test e non entrano in predict.
test_evaluation = test_features.merge(reference, on="observation_id", how="inner")

FEATURE_COLUMNS = ["duration_ms", "status_code"]
X_train = training_data[FEATURE_COLUMNS]
y_train = training_data["reference_label"]
X_test = test_evaluation[FEATURE_COLUMNS]
y_test = test_evaluation["reference_label"]

# MODIFICA GUIDATA - TASK 10
# Provare anche: DEPTHS = [1, 2, 4]
DEPTHS = [2, 4]

for depth in DEPTHS:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    # CODICE DI SERVIZIO
    train_correct = (train_predictions == y_train).sum()
    test_correct = (test_predictions == y_test).sum()

    tp = ((test_predictions == "anomaly") & (y_test == "anomaly")).sum()
    fp = ((test_predictions == "anomaly") & (y_test == "normal")).sum()
    fn = ((test_predictions == "normal") & (y_test == "anomaly")).sum()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    print(f"DEPTH {depth}")
    print(f"Training corretti: {train_correct}/{len(y_train)}")
    print(f"Test corretti: {test_correct}/{len(y_test)}")
    print("Precision test:", round(precision, 2))
    print("Recall test:", round(recall, 2))
    print()

# LIMITE DEL METODO
# La reference test serve soltanto per misurare le prediction.
# Non viene usata come feature e non entra nella chiamata predict().
