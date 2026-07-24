# Potenziamento 3 — Error analysis: che cosa non vede il modello?

## Livello

**Specifiche + struttura minima**

Tempo indicativo: **40–50 minuti**.

## Obiettivo

Passare dalle sole metriche aggregate ai singoli casi sbagliati.

Il modello principale ottiene:

```text
TP 7
FP 0
FN 2
TN 31
```

Il compito è capire **quali** sono i due falsi negativi e perché le feature disponibili non bastano.

## Starter

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/03_error_analysis_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/03_error_analysis.py
```

## Compiti

1. filtrare i casi in cui `prediction != reference_label`;
2. selezionare le colonne utili all'analisi;
3. esportare:

```text
POTENZIAMENTO_OPZIONALE/outputs/misclassified_cases.csv
```

4. raggruppare gli errori per `reference_reason_code`;
5. spiegare perché `duration_ms` e `status_code` non permettono di riconoscere quei casi.

## Vincolo

`reference_reason` e `label_source` possono essere letti **solo dopo la prediction**, durante l'analisi dell'errore.

Non devono diventare feature del modello: contengono informazioni del processo di validazione e potrebbero rivelare direttamente la risposta.

## Domanda finale

> Un modello può essere corretto al 95% e avere comunque un limite strutturale importante?

Rispondere usando i due falsi negativi reali del test.
