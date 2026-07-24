from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"

# UD29 - Script 02
# Obiettivo: comprendere che fit costruisce il modello usando feature + target di training.

training_data = pd.read_csv(TRAIN_PATH)
FEATURE_COLUMNS = ["duration_ms", "status_code"]
X_train = training_data[FEATURE_COLUMNS]
y_train = training_data["reference_label"]

# CONCETTO NUOVO
# max_depth=2 mantiene l'albero piccolo e leggibile.
# random_state rende l'esperimento ripetibile: è codice di servizio.
model = DecisionTreeClassifier(max_depth=2, random_state=42)

# CONCETTO NUOVO
# fit usa esempi (X_train) e risposte validate (y_train)
# per costruire le regole interne del modello.
model.fit(X_train, y_train)

print("Training completato.")
print("Osservazioni usate:", len(X_train))
print("Profondità dell'albero:", model.get_depth())
print("Numero di foglie:", model.get_n_leaves())

# LIMITE DEL METODO
# Aver completato il training non dimostra che il modello funzioni bene su dati nuovi.
