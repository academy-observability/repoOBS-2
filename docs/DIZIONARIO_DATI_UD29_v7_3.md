# UD29 — Dizionario dati

## File 1 — `ml_training_labeled.csv`

120 osservazioni storiche già validate, usate per il training.

Contiene sia le feature sia la `reference_label` perché durante `fit` il modello deve imparare da esempi con risposta nota.

Colonne:

| Colonna | Ruolo |
|---|---|
| `observation_id` | identificatore univoco |
| `timestamp_utc` | momento dell'osservazione |
| `environment` | ambiente |
| `service` | servizio osservato |
| `endpoint` | endpoint |
| `status_code` | feature usata dal modello come valore numerico; le soglie apprese non equivalgono automaticamente alla semantica HTTP |
| `duration_ms` | feature usata dal modello |
| `request_id` | correlazione richiesta |
| `trace_id` | correlazione trace |
| `reference_label` | target usato nel training |
| `reference_reason_code` | motivo sintetico della label |
| `reference_reason` | spiegazione della classificazione |
| `label_source` | processo/evidenza che ha prodotto la label |

---

## File 2 — `ml_test_features.csv`

40 osservazioni successive e separate dal training.

Serve per `predict`.

Contiene **solo dati osservativi**, non la risposta corretta.

Colonne:

| Colonna | Ruolo |
|---|---|
| `observation_id` | identificatore univoco |
| `timestamp_utc` | momento dell'osservazione |
| `environment` | ambiente |
| `service` | servizio |
| `endpoint` | endpoint |
| `status_code` | feature usata dal modello come valore numerico; le soglie apprese non equivalgono automaticamente alla semantica HTTP |
| `duration_ms` | feature usata dal modello |
| `request_id` | correlazione richiesta |
| `trace_id` | correlazione trace |

Assenti intenzionalmente:

```text
reference_label
reference_reason_code
reference_reason
label_source
```

---

## File 3 — `ml_test_reference_labels.csv`

40 classificazioni di riferimento, una per ogni `observation_id` del file `ml_test_features.csv`.

Serve **solo dopo la prediction** per valutare il modello.

| Colonna | Ruolo |
|---|---|
| `observation_id` | collega la reference alla stessa osservazione test |
| `reference_label` | classificazione di riferimento |
| `reference_reason_code` | motivo sintetico |
| `reference_reason` | spiegazione della classificazione |
| `label_source` | provenienza della validazione |

---

## File prodotto durante il laboratorio — `outputs/ml_test_predictions.csv`

Viene creato dallo script di prediction.

Contiene:

```text
observation_id
duration_ms
status_code
prediction
```

Non contiene la `reference_label`.

---

## Feature selezionate

```text
duration_ms
status_code
```

## Target del training

```text
reference_label
```

## Regola fondamentale

```text
FIT
vede feature + target

PREDICT
vede solo feature

EVALUATE
confronta prediction + reference
```


## Toy dataset per rendere visibile l'apprendimento

### `toy_ml_examples.csv`

Piccolo training set iniziale usato per mostrare le regole apprese dopo `fit()`.

### `toy_ml_examples_modified.csv`

Stesse colonne e stesso problema, ma alcuni esempi hanno valori differenti.
Serve a dimostrare che, mantenendo invariato il codice del modello, un nuovo training può produrre soglie apprese differenti.

I toy dataset non sostituiscono training e test reali: servono esclusivamente a rendere osservabile il concetto di apprendimento.
