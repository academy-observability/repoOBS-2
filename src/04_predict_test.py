from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"
TEST_FEATURES_PATH = ROOT / "datasets" / "ml_test_features.csv"
OUTPUT_PATH = ROOT / "outputs" / "ml_test_predictions.csv"

# UD29 - Script 03
# Obiettivo: produrre prediction su osservazioni test che NON contengono la reference_label.

training_data = pd.read_csv(TRAIN_PATH)
test_features = pd.read_csv(TEST_FEATURES_PATH)
FEATURE_COLUMNS = ["duration_ms", "status_code"]

X_train = training_data[FEATURE_COLUMNS]
y_train = training_data["reference_label"]

# CONCETTO NUOVO
# X_test contiene soltanto le feature.
# Nel file ml_test_features.csv non esiste la colonna reference_label.
X_test = test_features[FEATURE_COLUMNS]

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

# CONCETTO NUOVO
# predict applica le regole apprese a osservazioni senza risposta nota al modello.
predictions = model.predict(X_test)

# CODICE DI SERVIZIO
# Salviamo le prediction per poterle valutare in un secondo momento.
result = test_features[["observation_id", "duration_ms", "status_code"]].copy()
result["prediction"] = predictions
result.to_csv(OUTPUT_PATH, index=False)

print("Osservazioni test:", len(X_test))
print("Prediction prodotte:", len(predictions))
print("File creato:", OUTPUT_PATH)
print("\nPrime 10 prediction:")
print(result.head(10).to_string(index=False))

# LIMITE DEL METODO
# Qui non sappiamo ancora se le prediction siano corrette.
# La reference verrà consultata solo nella fase successiva di valutazione.
