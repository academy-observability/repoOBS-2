# UD28 — Laboratorio guidato
# Baseline, detector e valutazione

## Obiettivo

Seguiremo tre fasi distinte:

```text
FASE 1 → COSTRUIRE
baseline → mediana + MAD → soglia

FASE 2 → TESTARE
evaluation observations → detector → prediction

FASE 3 → VALUTARE
prediction + reference labels → TP/FP/FN/TN → precision/recall
```

---

# Task 1 — Capire i tre file prima del codice

Aprire soltanto i nomi dei file nella cartella `datasets/`.

```text
baseline_products_requests.csv
evaluation_products_requests.csv
products_reference_labels.csv
```

## Prima osservazione: i file non hanno tutti la stessa dimensione

```text
baseline_products_requests.csv   → 60 osservazioni
evaluation_products_requests.csv → 20 osservazioni
products_reference_labels.csv    → 20 label
```

Questa differenza è intenzionale:

- la baseline usa più osservazioni per costruire un punto di riferimento più rappresentativo;
- evaluation contiene un insieme più piccolo di nuove osservazioni da testare;
- reference contiene esattamente una label per ogni evaluation observation.

## Domande

1. Perché la baseline è più numerosa del file evaluation?
2. Quale file serve a costruire la soglia?
3. Quale file contiene le osservazioni da testare?
4. Perché evaluation e reference hanno lo stesso numero di righe?
5. Il reference file contiene nuove osservazioni?

Risposta all'ultima domanda:

> No. Contiene label e motivazioni riferite alle stesse `observation_id` del file evaluation.

---

# Task 2 — Calcolare MAD con cinque valori

Prima del codice:

```text
100 102 105 108 110
```

1. mediana = `105`;
2. distanze = `5, 3, 0, 3, 5`;
3. MAD = `3`.

Dobbiamo capire questo passaggio prima di usare pandas.

---

# Task 3 — Costruire la soglia dalla baseline

## File

```text
src/01_build_threshold.py
```

## Codice centrale

```python
median = durations.median()
distances = (durations - median).abs()
mad = distances.median()
threshold = median + multiplier * mad
```

Leggiamolo come una sequenza:

```text
durate baseline
→ mediana
→ distanza di ogni valore dalla mediana
→ mediana delle distanze = MAD
→ soglia
```

## Previsione

Con il dataset fornito ci aspettiamo:

```text
osservazioni baseline = 60
mediana = 166,5
MAD = 7,5
soglia con moltiplicatore 4 = 196,5
```

## Esecuzione

```bash
python src/01_build_threshold.py
```

## Domanda

La soglia `196,5` è una legge universale?

No. Dipende dalla baseline e dal moltiplicatore scelto.

---

# Task 4 — Applicare la soglia alle evaluation observations

## File

```text
src/02_detect_candidates.py
```

Il detector usa soltanto:

```text
duration_ms
```

Regola:

```python
evaluation["predicted_label"] = "normal"
evaluation.loc[evaluation["duration_ms"] > threshold, "predicted_label"] = "anomaly"
```

La sintassi `.loc` è spiegata nel file, ma il concetto da comprendere è:

```text
se duration_ms > soglia
→ prediction anomaly
altrimenti
→ prediction normal
```

## Esecuzione

```bash
python src/02_detect_candidates.py
```

Viene creato:

```text
outputs/predictions.csv
```

### Fermiamoci

A questo punto abbiamo soltanto **prediction**.

Non sappiamo ancora quanti casi siano corretti.

---

# Task 5 — Chi crea il reference file?

Prima di aprirlo, discutiamo il processo reale.

```text
telemetria
+ test controllati
+ incident review
+ conoscenza del servizio
        ↓
SRE / Operations / Service Owner / QA
        ↓
validazione indipendente
        ↓
reference labels
```

Nel laboratorio il CSV rappresenta il risultato di questo processo.

## Aprire ora

```text
datasets/products_reference_labels.csv
```

Osservare:

```text
reference_label
reference_reason_code
reference_reason
label_source
```

## Importante

`reference_reason` spiega **perché è stata assegnata la label**.

Non identifica automaticamente la root cause tecnica.

---

# Task 6 — Leggere il reference file senza fare ancora il confronto

## File

```text
src/03_inspect_reference_labels.py
```

## Esecuzione

```bash
python src/03_inspect_reference_labels.py
```

Lo script mostra tutte le observation_id con:

- label;
- motivo;
- provenienza della validazione.

## Domanda

Perché troviamo `eval-005` sia nel file evaluation sia nel reference file?

Perché è la **stessa osservazione**:

```text
evaluation → dati osservati
reference  → classificazione di riferimento
```

---

# Task 7 — Confrontare prediction e reference

## File

```text
src/04_compare_prediction_reference.py
```

Il codice di servizio associa i due file usando:

```text
observation_id
```

Schema:

```text
predictions.csv                  reference_labels.csv
     eval-005 ----------------------- eval-005
            \                         /
             \                       /
              → stessa osservazione ←
```

## Esecuzione

```bash
python src/04_compare_prediction_reference.py
```

Viene creato:

```text
outputs/comparison.csv
```

---

# Task 8 — Capire TP, FP, FN e TN sui casi reali

Aprire `outputs/comparison.csv`.

Con soglia `196,5 ms` troviamo:

```text
TP = 4
FP = 2
FN = 1
TN = 13
```

Non memorizziamo solo i numeri. Guardiamo i casi.

### TP

Prediction e reference dicono entrambe `anomaly`.

### FP

Il detector segnala una anomaly, ma il processo di validazione considera il caso normal.

### FN

Il detector dice normal, ma la reference dice anomaly.

---

# Task 9 — Analizzare concretamente il falso negativo

Il falso negativo è:

```text
observation_id = eval-005
```

Dati dell'osservazione:

```text
duration_ms = 190
status_code = 500
```

## Che cosa vede il detector?

Il detector usa soltanto `duration_ms`:

```text
190 < 196,5
→ predicted_label = normal
```

## Che cosa dice la reference?

```text
reference_label = anomaly
reference_reason_code = unexpected_error
reference_reason = Risposta HTTP 500 inattesa confermata durante la revisione tecnica del caso
label_source = incident_review
```

## Perché c'è differenza?

```text
OSSERVAZIONE eval-005
        │
        ├── duration_ms = 190 ──→ detector → normal
        │
        └── status_code = 500 ──→ validazione tecnica → anomaly
```

Il detector non usa `status_code`, quindi non può riconoscere questo tipo di problema se la durata non supera la soglia.

### Domanda importante

Il reference file ha “scoperto” l'errore dopo una seconda osservazione?

No.

La richiesta è sempre `eval-005`. Il reference file contiene informazioni di validazione raccolte o formalizzate a posteriori sulla **stessa richiesta**.

---

# Task 10 — Analizzare concretamente un falso positivo

Uno dei falsi positivi è:

```text
eval-003
```

```text
duration_ms = 205
status_code = 200
```

Detector:

```text
205 > 196,5
→ anomaly
```

Reference:

```text
normal
reference_reason = Picco transitorio di latenza considerato accettabile dal service owner per questo scenario
label_source = service_review
```

Questo mostra che:

```text
superare una soglia statistica
≠
incidente confermato
```

---

# Task 11 — Precision e recall

## File

```text
src/05_evaluate_detector.py
```

## Esecuzione

```bash
python src/05_evaluate_detector.py
```

Risultati:

```text
precision ≈ 0,67
recall = 0,80
```

Interpretazione:

- tra i 6 casi segnalati, 4 sono anomaly secondo la reference: circa il 67%;
- tra le 5 anomaly presenti nella reference, il detector ne trova 4: 80%.

---

# Task 12 — Modificare la soglia e osservare il compromesso

## File

```text
src/06_compare_two_thresholds.py
```

Confrontiamo:

```text
moltiplicatore 4 → soglia 196,5
moltiplicatore 3 → soglia 189
```

## Esecuzione

```bash
python src/06_compare_two_thresholds.py
```

Risultati:

```text
moltiplicatore 4
TP 4 FP 2 FN 1 TN 13
precision ≈ 0,67
recall 0,80

moltiplicatore 3
TP 5 FP 3 FN 0 TN 12
precision = 0,625
recall 1,00
```

## Interpretazione

Abbassando la soglia:

- recuperiamo `eval-005`;
- ma segnaliamo anche più casi che la reference considera normal.

Questo è un **compromesso**, non una vittoria automatica.

---

# Criterio di completamento

Dobbiamo saper spiegare:

1. perché baseline ed evaluation contengono osservazioni differenti;
2. perché evaluation e reference condividono le stesse `observation_id`;
3. chi può contribuire alla ground truth in un contesto reale;
4. differenza tra `reference_reason` e root cause;
5. perché `eval-005` è un falso negativo;
6. perché `eval-003` è un falso positivo;
7. come una soglia diversa modifica precision e recall.
