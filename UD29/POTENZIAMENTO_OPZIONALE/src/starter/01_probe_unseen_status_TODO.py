from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# CODICE DI SERVIZIO
# Copiare questo file nella cartella POTENZIAMENTO_OPZIONALE/src prima di eseguirlo.
ROOT = Path(__file__).resolve().parents[2]
TOY_PATH = ROOT / "datasets" / "toy_ml_examples.csv"
OUTPUT_PATH = ROOT / "POTENZIAMENTO_OPZIONALE" / "outputs" / "potenziamento_01_synthetic_probe.csv"

data = pd.read_csv(TOY_PATH)
X = data[["duration_ms", "status_code"]]
y = data["reference_label"]

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X, y)

print("Regole apprese:")
print(export_text(model, feature_names=["duration_ms", "status_code"]))

# TODO 1
# Inserire i quattro status richiesti dalla consegna.
PROBE_STATUS_CODES = None

if PROBE_STATUS_CODES is None:
    raise SystemExit("Completare TODO 1: PROBE_STATUS_CODES")

# TODO 2
# Costruire un DataFrame con duration_ms=170 per ogni status.
probe = None

if probe is None:
    raise SystemExit("Completare TODO 2: costruire probe")

# CONCETTO UD29
probe["prediction"] = model.predict(probe[["duration_ms", "status_code"]])

# CODICE DI SERVIZIO
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
probe.to_csv(OUTPUT_PATH, index=False)
print("\nCasi sondati:")
print(probe.to_string(index=False))
print("\nOutput:", OUTPUT_PATH)

# INTERPRETAZIONE
# La soglia appresa su status_code è una separazione numerica del training set.
# Non equivale automaticamente a una regola del protocollo HTTP.
