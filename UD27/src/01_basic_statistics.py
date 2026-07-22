# UD27 - Script 01
# Obiettivo: descrivere le durate con poche statistiche di base.

from pathlib import Path
import pandas as pd

# CODICE DI SERVIZIO
# Costruiamo il percorso del dataset partendo dalla posizione dello script.
DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "mini_products_requests.csv"

# CONCETTO GIÀ CONOSCIUTO DA UD26
# Leggiamo il CSV e otteniamo un DataFrame.
data = pd.read_csv(DATASET_PATH)

# CONCETTO GIÀ CONOSCIUTO DA UD26
# Selezioniamo la colonna che contiene le durate in millisecondi.
durations = data["duration_ms"]

# MODIFICA GUIDATA - TASK 3
# Sostituire temporaneamente la riga precedente con:
# durations = data["duration_ms"].head(5)
# In questo modo descriveremo soltanto le prime cinque durate.

# CONCETTO NUOVO
# Queste funzioni riassumono l'insieme di valori selezionato.
print("Count:", durations.count())
print("Minimo:", round(durations.min(), 2), "ms")
print("Massimo:", round(durations.max(), 2), "ms")
print("Media:", round(durations.mean(), 2), "ms")
print("Mediana:", round(durations.median(), 2), "ms")

# LIMITE DEL METODO
# Queste statistiche descrivono tutte le durate mescolate insieme.
# Nel dataset esistono endpoint con comportamenti differenti: nel prossimo script
# analizzeremo un gruppo più coerente.
