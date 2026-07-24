# UD29 — Guida operativa

## 1. Ambiente virtuale

Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Installazione

```bash
python -m pip install -r requirements.txt
```

Verifica:

```bash
python -c "import pandas, sklearn; print('pandas', pandas.__version__); print('sklearn', sklearn.__version__)"
```

## 3. Dataset

### Toy dataset per vedere l’apprendimento

```text
datasets/toy_ml_examples.csv
datasets/toy_ml_examples_modified.csv
```

Servono soltanto a mostrare che lo stesso codice, riaddestrato su esempi differenti, può apprendere regole differenti.

### Dataset del caso completo

```text
datasets/ml_training_labeled.csv         120 osservazioni + label
datasets/ml_test_features.csv             40 osservazioni senza label
datasets/ml_test_reference_labels.csv     40 reference label separate
```

Verifiche importanti:

```text
training observation_id ≠ test observation_id

test features observation_id
=
test reference observation_id
```

## 4. Esecuzione nell'ordine corretto

```bash
python src/01_learning_from_examples.py
python src/02_features_and_target.py
python src/03_train_decision_tree.py
python src/04_predict_test.py
python src/05_evaluate_model.py
python src/06_read_tree_rules.py
python src/07_compare_depths.py
```

Lo script 04 crea:

```text
outputs/ml_test_predictions.csv
```

Lo script 05 usa questo file e solo allora apre:

```text
ml_test_reference_labels.csv
```

## 5. Codice centrale

Dobbiamo comprendere:

```text
fit come momento di apprendimento
FEATURE_COLUMNS
X_train
y_train
X_test
DecisionTreeClassifier
fit
predict
max_depth
```

## 6. Codice di servizio

Sono forniti e commentati:

- costruzione dei percorsi;
- salvataggio delle prediction;
- `merge` tra prediction e reference tramite `observation_id`;
- conteggio TP/FP/FN/TN;
- formattazione dell'output;
- stampa testuale dell'albero.

Non è richiesto ricostruirli da zero.
