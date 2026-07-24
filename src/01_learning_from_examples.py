# UD29 - Script 01
# Obiettivo: rendere visibile che durante fit() il Decision Tree
# apprende regole dai dati invece di ricevere soglie scritte da noi.

from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# CODICE DI SERVIZIO
ROOT = Path(__file__).resolve().parents[1]

# MODIFICA GUIDATA - TASK 4
# Prima eseguire con il dataset iniziale.
TOY_DATASET_PATH = ROOT / "datasets" / "toy_ml_examples.csv"
# Poi sostituire temporaneamente la riga precedente con:
# TOY_DATASET_PATH = ROOT / "datasets" / "toy_ml_examples_modified.csv"
# Il codice del modello e di fit() resterà identico.

data = pd.read_csv(TOY_DATASET_PATH)

# CONCETTO NUOVO
# X contiene le feature che il modello può osservare.
X = data[["duration_ms", "status_code"]]

# y contiene le risposte note usate per apprendere durante il training.
y = data["reference_label"]

# IMPORTANTE
# Qui NON scriviamo regole come:
# if duration_ms > 205: anomaly
# if status_code == 500: anomaly
# Dichiariamo soltanto il tipo di algoritmo e un limite di complessità.
model = DecisionTreeClassifier(max_depth=2, random_state=42)

print("Dataset usato:", TOY_DATASET_PATH.name)
print("\nEsempi di training:")
print(data.to_string(index=False))

print("\nPRIMA DI fit():")
print(
    "Il DecisionTreeClassifier è stato creato, "
    "ma non ha ancora appreso regole dai dati."
)

# CONCETTO CENTRALE DELLA UD
# fit() osserva esempi + risposte note e costruisce le regole interne.
model.fit(X, y)

# CODICE DI SERVIZIO
# export_text rende leggibili le regole apprese.
rules = export_text(model, feature_names=["duration_ms", "status_code"])

print("\nDOPO fit():")
print("Regole apprese dai dati:")
print(rules)

# LIMITE DEL METODO
# Il modello non apprende "spontaneamente" qualsiasi cosa:
# siamo noi a scegliere feature, target, algoritmo e max_depth.
# All'interno di questi vincoli, fit() apprende dai dati separazioni e soglie.

# NOTA DI INTERPRETAZIONE
# Se export_text mostra una soglia come status_code <= 350,
# 350 NON è una regola HTTP: è una separazione numerica appresa
# dagli esempi disponibili. Il modello non conosce automaticamente
# la semantica del protocollo o il contratto operativo del servizio.
