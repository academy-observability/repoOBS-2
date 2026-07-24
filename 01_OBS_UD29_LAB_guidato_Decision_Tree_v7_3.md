# UD29 — Laboratorio guidato
# Vedere l'apprendimento prima della prediction

## Obiettivo

Alla fine dobbiamo distinguere con chiarezza:

```text
fit()      = apprendimento
predict()  = inferenza
evaluation = verifica delle prediction
```

Il laboratorio parte da un esempio minuscolo prima di usare i dataset completi.

---

# Task 1 — Collegamento con UD28

In UD28 avevamo una regola esplicita:

```text
threshold = mediana + 4 × MAD
duration_ms > threshold → anomaly candidate
```

Rispondere:

> Chi aveva definito la formula e il moltiplicatore?

Risposta: noi.

In UD29 vogliamo vedere che alcune regole possono invece essere **apprese dagli esempi**.

---

# Task 2 — Guardare il toy dataset prima del codice

Aprire:

```text
datasets/toy_ml_examples.csv
```

Osservare che:

- le durate 150–180 con status 200 sono `normal`;
- 230 e 250 con status 200 sono `anomaly`;
- 165 con status 500 è `anomaly` nonostante la durata sia bassa.

## Domanda

Se dovessimo scrivere noi una regola, quali condizioni proveremmo?

Non serve trovare la soluzione perfetta. Serve riconoscere che esistono più segnali.

---

# Task 3 — Vedere `fit()` costruire le regole

## File

```text
src/01_learning_from_examples.py
```

## Prima dell'esecuzione

Cercare:

```python
model = DecisionTreeClassifier(max_depth=2, random_state=42)
```

Nel codice non compare nessuna riga come:

```python
if duration_ms > 205:
    ...
```

né:

```python
if status_code == 500:
    ...
```

Poi troviamo:

```python
model.fit(X, y)
```

### Significato

```text
X = esempi osservabili
y = risposte note
      ↓
     fit()
      ↓
regole apprese
```

## Previsione

Prima di `fit()` abbiamo scelto il tipo di modello, ma non abbiamo scritto le soglie operative.

Dopo `fit()` ci aspettiamo di poter leggere regole costruite dagli esempi.

## Esecuzione

```bash
python src/01_learning_from_examples.py
```

Individuare nella stampa una soglia vicina a:

```text
duration_ms <= 205
```

## Domanda fondamentale

Dove compare `205` nel codice sorgente?

Risposta: **non compare**. È il risultato dell'apprendimento sui dati.

## Task 3B — Interpretare correttamente `status_code <= 350`

Nell'albero del toy dataset compare anche una separazione simile a:

```text
status_code <= 350?
```

Non leggerla come una regola HTTP.

Il modello ha ricevuto `status_code` come numero e, negli esempi disponibili, ha visto soprattutto `200` e `500`. La soglia è una separazione numerica appresa per distinguere quegli esempi.

### Caso da ragionare insieme

```text
duration_ms = 170
status_code = 300
```

Seguendo l'albero:

```text
170 <= 205 → sì
300 <= 350 → sì
prediction  → normal
```

Domande:

1. questo significa che HTTP considera sempre `300` “normale”? **No**;
2. significa che il modello conosce la semantica dei codici HTTP? **No**;
3. che cosa significa allora `350`? **È una soglia numerica appresa dagli esempi disponibili**;
4. un `3xx` può essere anomalo per uno specifico servizio? **Sì, se rappresenta un comportamento inatteso rispetto al contratto o al contesto operativo**.

> Distinguere sempre **regola appresa**, **semantica del dominio** e **valutazione operativa**.

---

# Task 4 — Cambiare i dati e riaddestrare

Nello stesso file cercare:

```python
# MODIFICA GUIDATA - TASK 4
```

Sostituire temporaneamente:

```python
TOY_DATASET_PATH = ROOT / "datasets" / "toy_ml_examples.csv"
```

con:

```python
TOY_DATASET_PATH = ROOT / "datasets" / "toy_ml_examples_modified.csv"
```

Non modificare:

```python
DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X, y)
```

## Prima di eseguire

Aprire il dataset modificato e osservare che alcuni esempi `normal` e `anomaly` si sono spostati verso durate più alte.

## Esecuzione

```bash
python src/01_learning_from_examples.py
```

Ora la soglia principale appresa è vicina a:

```text
duration_ms <= 250
```

## Conclusione da formulare

```text
stesso algoritmo
+ stesso codice
+ dati differenti
= regole apprese differenti
```

Questo è il passaggio in cui deve diventare visibile il Machine Learning.

### Ripristino

Ripristinare `toy_ml_examples.csv` come dataset iniziale.

---

# Task 5 — Feature e target nel training reale

## File

```text
src/02_features_and_target.py
```

Comprendere:

```python
FEATURE_COLUMNS = ["duration_ms", "status_code"]
X_train = training_data[FEATURE_COLUMNS]
y_train = training_data["reference_label"]
```

```text
X_train → ciò che il modello osserva
y_train → risposta da apprendere
```

## Esecuzione

```bash
python src/02_features_and_target.py
```

## Modifica guidata

Provare temporaneamente:

```python
FEATURE_COLUMNS = ["duration_ms"]
```

Domanda:

> Quale informazione non potrà più utilizzare il modello durante l'apprendimento?

Ripristinare entrambe le feature.

---

# Task 6 — Training completo: `fit()`

## File

```text
src/03_train_decision_tree.py
```

Il concetto è già stato visto sul toy dataset.

Ora lo applichiamo a 120 osservazioni storiche validate:

```python
model.fit(X_train, y_train)
```

## Esecuzione

```bash
python src/03_train_decision_tree.py
```

Il risultato ci dice che il modello è stato costruito.

Non dimostra ancora che generalizzi bene.

---

# Task 7 — Prima dell'inferenza: test senza risposta

Aprire:

```text
datasets/ml_test_features.csv
```

Verificare che non contenga:

```text
reference_label
reference_reason
label_source
```

## Domanda

Perché?

Perché `predict()` deve ricevere le feature e produrre una risposta senza che il modello conosca già la soluzione.

---

# Task 8 — `predict()` = inferenza

## File

```text
src/04_predict_test.py
```

Individuare:

```python
predictions = model.predict(X_test)
```

Questo non è più apprendimento.

```text
modello già appreso + nuovi dati
            ↓
         predict()
            ↓
         inference
```

## Esecuzione

```bash
python src/04_predict_test.py
```

Viene creato:

```text
outputs/ml_test_predictions.csv
```

A questo punto abbiamo prediction, non ancora la verifica della loro correttezza.

---

# Task 9 — Aprire la reference solo dopo

Ora aprire:

```text
datasets/ml_test_reference_labels.csv
```

Le `test-*` sono le stesse osservazioni del test features.

Il file funziona come foglio delle risposte per la valutazione.

Non entra in `predict()`.

---

# Task 10 — Valutare il modello

## File

```text
src/05_evaluate_model.py
```

## Esecuzione

```bash
python src/05_evaluate_model.py
```

Risultato atteso:

```text
TP = 7
FP = 0
FN = 2
TN = 31
precision = 1,00
recall ≈ 0,78
```

Interpretazione:

- quando segnala `anomaly`, nei 40 casi di test non produce falsi positivi;
- trova 7 delle 9 anomaly validate;
- ne perde 2 perché le feature disponibili non contengono tutte le evidenze usate nel processo di validazione.

---

# Task 11 — Leggere le regole apprese sul training completo

## File

```text
src/06_read_tree_rules.py
```

## Esecuzione

```bash
python src/06_read_tree_rules.py
```

Confrontare con UD28:

```text
UD28 → regola definita da noi
UD29 → regole apprese durante fit()
```

---

# Task 12 — Overfitting intuitivo

## File

```text
src/07_compare_depths.py
```

## Esecuzione

```bash
python src/07_compare_depths.py
```

Risultato validato:

```text
depth 2 → training 113/120, test 38/40
depth 4 → training 114/120, test 36/40
```

Il modello più complesso migliora leggermente sul training e peggiora sul test.

```text
adattarsi meglio al training
≠
generalizzare meglio
```

### Modifica guidata

Provare:

```python
DEPTHS = [1, 2, 4]
```

---

# Task 13 — Evidenza finale

Completare:

```text
templates/evidence_ud29_template.md
```

Alla fine dobbiamo saper spiegare con parole nostre:

1. che cosa esiste prima di `fit()`;
2. che cosa viene appreso durante `fit()`;
3. perché cambiando i dati possono cambiare le regole;
4. differenza tra `fit()` e `predict()`;
5. perché la reference test resta separata;
6. perché un modello può comunque sbagliare.
