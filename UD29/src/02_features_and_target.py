from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "datasets" / "ml_training_labeled.csv"

# UD29 - Script 01
# Obiettivo: distinguere feature (X) e target (y) nel training.

training_data = pd.read_csv(TRAIN_PATH)

# CONCETTO NUOVO
# Queste sono le sole informazioni operative che il modello potrà osservare.
FEATURE_COLUMNS = ["duration_ms", "status_code"]

# MODIFICA GUIDATA
# Provare temporaneamente con:
# FEATURE_COLUMNS = ["duration_ms"]

X_train = training_data[FEATURE_COLUMNS]

# Nel training la reference_label è il target: la risposta nota da apprendere.
y_train = training_data["reference_label"]

print("Righe training:", len(training_data))
print("Feature:", FEATURE_COLUMNS)
print("Forma di X_train:", X_train.shape)
print("Numero di target in y_train:", len(y_train))
print("\nPrime feature:")
print(X_train.head())
print("\nPrime label:")
print(y_train.head())

# LIMITE DEL METODO
# reference_reason e label_source non fanno parte di X:
# sono informazioni di validazione che potrebbero suggerire la risposta.
