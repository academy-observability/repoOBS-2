# UD28 — Baseline e anomaly detection statistica

## Domanda guida

> Come definiamo un comportamento di riferimento e segnaliamo gli scostamenti da verificare?

In UD27 abbiamo imparato a **descrivere** i dati con media, mediana, p95 e gruppi.

Ora facciamo un solo salto concettuale:

```text
comportamento osservato
        ↓
comportamento di riferimento
        ↓
confronto
        ↓
anomaly candidate
```

## I tre ruoli dei dati

```text
baseline_products_requests.csv
→ COSTRUIRE il riferimento e la soglia

evaluation_products_requests.csv
→ TESTARE il detector su osservazioni successive

products_reference_labels.csv
→ VALUTARE le prediction sulle stesse observation_id del file evaluation
```

Le numerosità sono volutamente diverse:

```text
baseline   = 60 osservazioni
evaluation = 20 osservazioni
reference  = 20 label, una per ogni evaluation observation
```

La baseline è più ampia perché deve fornire un punto di riferimento costruito su un insieme più rappresentativo.
Evaluation e reference hanno invece la stessa numerosità perché sono in relazione 1:1 tramite `observation_id`.

Il reference file **non contiene nuove osservazioni**. Contiene informazioni di validazione riferite alle stesse `observation_id` del file di evaluation.

## In questa UD

- baseline;
- mediana e MAD;
- soglia;
- anomaly candidate;
- ground truth / reference label;
- reference reason e label source;
- TP, FP, FN, TN;
- precision e recall.

## Non ancora

- training ML;
- `fit` e `predict` di un modello;
- Decision Tree;
- Isolation Forest;
- AI generativa.
