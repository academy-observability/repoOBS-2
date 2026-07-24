from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[2]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_PATH = ROOT / "datasets" / "ml_test_features.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"
FEATURES = ["duration_ms", "status_code"]

train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH).merge(
    pd.read_csv(REFERENCE_PATH), on="observation_id", how="inner"
)

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(train[FEATURES], train["reference_label"])

print("ALBERO APPRESO")
print(export_text(model, feature_names=FEATURES))

# TODO 1
CASE_IDS = None

if CASE_IDS is None:
    raise SystemExit("Completare TODO 1: CASE_IDS")

# CODICE DI SERVIZIO
def explain_path(row):
    """Rende leggibile il percorso interno dell'albero per una singola riga."""
    X_row = row[FEATURES].to_frame().T
    node_indicator = model.decision_path(X_row)
    leaf_id = model.apply(X_row)[0]
    tree = model.tree_
    feature_names = FEATURES

    lines = []
    node_ids = node_indicator.indices[node_indicator.indptr[0]:node_indicator.indptr[1]]
    for node_id in node_ids:
        if node_id == leaf_id:
            lines.append(f"leaf {node_id}")
            continue
        feature_index = tree.feature[node_id]
        threshold = tree.threshold[node_id]
        feature = feature_names[feature_index]
        value = float(row[feature])
        operator = "<=" if value <= threshold else ">"
        lines.append(f"{feature}={value:g} {operator} {threshold:.2f}")
    return " | ".join(lines)

selected = test[test["observation_id"].isin(CASE_IDS)].copy()
selected["prediction"] = model.predict(selected[FEATURES])
selected["decision_path"] = selected.apply(explain_path, axis=1)

print("\nCASI SELEZIONATI")
for _, row in selected.iterrows():
    print("\n", row["observation_id"])
    print("duration_ms:", row["duration_ms"], "status_code:", row["status_code"])
    print("path:", row["decision_path"])
    print("prediction:", row["prediction"], "reference:", row["reference_label"])
    print("reason:", row["reference_reason_code"])
