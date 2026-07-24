# UD29 — Machine Learning spiegabile

## Domanda guida

> Che cosa significa realmente che un modello **apprende dai dati**?

In UD28 abbiamo costruito noi una regola statistica:

```text
baseline → mediana + MAD → soglia → anomaly candidate
```

In UD29 facciamo un solo nuovo salto:

```text
regola definita da noi
        ↓
regola appresa dagli esempi durante fit()
```

Il punto centrale non è soltanto ottenere una prediction. Prima dobbiamo **vedere l'apprendimento**.

Un secondo punto da rendere esplicito è:

```text
soglia appresa ≠ regola del dominio
```

Per esempio, se il Decision Tree apprende `status_code <= 350`, quella soglia descrive una separazione numerica utile sugli esempi di training: non è una regola ufficiale dei codici HTTP.

```text
esempi + risposte note
        ↓
       fit()
        ↓
regole e soglie apprese
        ↓
      modello
        ↓
nuovi dati senza label
        ↓
     predict()
        ↓
    prediction
```

## Esperimento iniziale

Usiamo due toy dataset quasi uguali:

```text
toy_ml_examples.csv
toy_ml_examples_modified.csv
```

Il codice del modello resta identico. Cambiano soltanto alcuni esempi.

Il risultato osservabile è:

```text
dati iniziali  → soglia appresa circa 205 ms
dati modificati → soglia appresa circa 250 ms
```

Quindi:

> stesso algoritmo + stesso codice + dati differenti = modello appreso differente.

## In questa UD impariamo

- che cosa avviene durante `fit()`;
- differenza tra apprendimento e inferenza;
- feature e target;
- training e test;
- Decision Tree semplice e spiegabile;
- `predict()` su dati senza label;
- valutazione con TP/FP/FN/TN, precision e recall già conosciuti;
- idea intuitiva di overfitting.

## Tre ruoli dei dati reali

```text
ml_training_labeled.csv
→ feature + reference_label note
→ serve per FIT

ml_test_features.csv
→ solo dati osservabili dal modello
→ serve per PREDICT

ml_test_reference_labels.csv
→ risposte di riferimento delle stesse test-*
→ serve DOPO la prediction per VALUTARE
```

## Non stiamo facendo

- molti algoritmi ML;
- reti neurali;
- tuning avanzato;
- scaling e preprocessing complesso;
- Azure ML;
- AI generativa.

## Un solo modello principale

`DecisionTreeClassifier`, perché rende leggibili le regole apprese.

## Ordine consigliato

1. `00_OBS_UD29_Concetti_ML_Spiegabile_v7_3.md`
2. `02_OBS_UD29_ESEMPI_VISIVI_E_NUMERICI_v7_3.md`
3. `01_OBS_UD29_LAB_guidato_Decision_Tree_v7_3.md`
4. `03_OBS_UD29_MINI_ATTIVITA_v7_3.md`
5. `04_OBS_UD29_LAB_autonomo_Confrontare_Feature_v7_3.md`
6. `06_OBS_UD29_Raccordo_Verso_AI_v7_3.md`
7. `POTENZIAMENTO_OPZIONALE/README_POTENZIAMENTO_UD29_v1_0.md` — facoltativo, dopo il percorso principale.

## Competenza finale

> So distinguere training e inferenza e so spiegare che durante `fit()` il modello apprende dai dati regole e soglie che non sono state programmate esplicitamente; so poi usare `predict()` su dati senza label e valutare le prediction con una reference separata.
