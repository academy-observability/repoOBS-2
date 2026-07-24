from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"

# UD29 - Script 05
# Obiettivo: leggere in forma testuale le regole apprese dal Decision Tree.

training_data = pd.read_csv(TRAIN_PATH)
FEATURE_COLUMNS = ["duration_ms", "status_code"]
X_train = training_data[FEATURE_COLUMNS]
y_train = training_data["reference_label"]

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

# CODICE DI SERVIZIO
# export_text trasforma l'albero in un testo leggibile.
rules = export_text(model, feature_names=FEATURE_COLUMNS)

print("REGOLE APPRESE DAL MODELLO")
print(rules)

# DOMANDA GUIDA
# Quale regola permette di riconoscere status_code 500 anche con durata non elevata?
# Attenzione: una soglia numerica come 350 non è una regola HTTP.
# È una separazione appresa dal training set.
