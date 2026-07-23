# UD28 - Script 01
# Obiettivo: costruire una soglia a partire dalle osservazioni di baseline.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
BASELINE_PATH = Path(__file__).resolve().parents[1] / "datasets" / "baseline_products_requests.csv"

baseline = pd.read_csv(BASELINE_PATH)
durations = baseline["duration_ms"]

# CONCETTO NUOVO
# La mediana rappresenta il centro robusto della baseline.
median = durations.median()

# Calcoliamo di quanto ogni durata si allontana dalla mediana.
distances = (durations - median).abs()

# Il MAD è la mediana di queste distanze.
mad = distances.median()

# MODIFICA GUIDATA
# Il moltiplicatore è una scelta tecnica dell'esperimento.
multiplier = 4
threshold = median + multiplier * mad

print("Osservazioni baseline:", len(baseline))
print("Mediana:", median, "ms")
print("MAD:", mad, "ms")
print("Moltiplicatore:", multiplier)
print("Soglia:", threshold, "ms")

# LIMITE DEL METODO
# La soglia dipende dalla baseline e dal moltiplicatore scelto.
# Non è una legge universale.
