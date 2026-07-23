# UD28 - Script 02
# Obiettivo: applicare la soglia alle observation del file evaluation.

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "datasets" / "baseline_products_requests.csv"
EVALUATION_PATH = ROOT / "datasets" / "evaluation_products_requests.csv"
OUTPUT_PATH = ROOT / "outputs" / "predictions.csv"

# CODICE DI SERVIZIO
baseline = pd.read_csv(BASELINE_PATH)
evaluation = pd.read_csv(EVALUATION_PATH)

median = baseline["duration_ms"].median()
mad = (baseline["duration_ms"] - median).abs().median()
multiplier = 4
threshold = median + multiplier * mad

# CONCETTO NUOVO
# Inizialmente consideriamo tutte le observation come normal.
evaluation["predicted_label"] = "normal"

# Le sole observation con durata sopra soglia diventano anomaly candidate.
# .loc significa: modifica la colonna predicted_label soltanto nelle righe
# che soddisfano la condizione indicata.
evaluation.loc[
    evaluation["duration_ms"] > threshold,
    "predicted_label"
] = "anomaly"

evaluation["threshold_ms"] = threshold

evaluation.to_csv(OUTPUT_PATH, index=False)

print("Soglia:", threshold, "ms")
print(evaluation[["observation_id", "duration_ms", "status_code", "predicted_label"]].to_string(index=False))
print("\nPrediction salvate in:", OUTPUT_PATH)

# LIMITE DEL METODO
# Il detector usa SOLO duration_ms.
# Non usa status_code, log, trace o informazioni di validazione.
