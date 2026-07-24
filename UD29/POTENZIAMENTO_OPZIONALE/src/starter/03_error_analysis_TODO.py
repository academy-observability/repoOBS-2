from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[2]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_PATH = ROOT / "datasets" / "ml_test_features.csv"
REFERENCE_PATH = ROOT / "datasets" / "ml_test_reference_labels.csv"
OUTPUT_PATH = ROOT / "POTENZIAMENTO_OPZIONALE" / "outputs" / "misclassified_cases.csv"
FEATURES = ["duration_ms", "status_code"]

train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)
reference = pd.read_csv(REFERENCE_PATH)

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(train[FEATURES], train["reference_label"])

predictions = model.predict(test[FEATURES])
predicted = test.copy()
predicted["prediction"] = predictions

# CODICE DI SERVIZIO
# La reference entra soltanto ora, dopo predict().
evaluation = predicted.merge(reference, on="observation_id", how="inner")

# TODO 1
# Filtrare soltanto i casi con prediction diversa da reference_label.
errors = None

if errors is None:
    raise SystemExit("Completare TODO 1: errors")

# TODO 2
# Selezionare almeno:
# observation_id, duration_ms, status_code, prediction, reference_label,
# reference_reason_code, reference_reason, label_source
columns = None

if columns is None:
    raise SystemExit("Completare TODO 2: columns")

result = errors[columns].copy()

# CODICE DI SERVIZIO
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT_PATH, index=False)

print("Casi errati:")
print(result.to_string(index=False))
print("\nErrori per reason code:")
print(result["reference_reason_code"].value_counts().to_string())
print("\nOutput:", OUTPUT_PATH)
