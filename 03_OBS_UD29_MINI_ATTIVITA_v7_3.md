# UD29 — Mini-attività

## Attività 1 — Programmazione o apprendimento?

Indicare quale frase descrive UD28 e quale UD29:

A. “Scriviamo noi la formula che produce la soglia.”
B. “Forniamo esempi e label; `fit()` costruisce regole e soglie interne.”

---

## Attività 2 — Dov'è la soglia?

Nel codice:

```python
model = DecisionTreeClassifier(max_depth=2)
model.fit(X, y)
```

dopo il training compare una soglia `205` nell'albero.

Rispondere:

1. era scritta nel codice?
2. da dove deriva?

---


## Attività 3 — La soglia 350 è una regola HTTP?

L'albero appreso mostra:

```text
status_code <= 350?
```

Rispondere:

1. `350` è una soglia definita dallo standard HTTP?
2. perché può essere comparsa proprio tra `200` e `500`?
3. con `duration_ms=170` e `status_code=300`, quale ramo segue il modello?
4. perché la prediction ottenuta non basta, da sola, a stabilire se il comportamento è corretto per il servizio?

---
## Attività 4 — Stesso codice, dati diversi

Completare:

```text
stesso algoritmo + stessi parametri + dati di training differenti
→ __________________________________________
```

Spiegare perché questo mostra l'apprendimento.

---

## Attività 5 — Fit o predict?

Associare:

- costruisce il modello dagli esempi;
- applica il modello a nuovi dati;

a:

```text
fit()
predict()
```

---

## Attività 6 — Chi decide cosa?

Separare tra **decisione umana/progettuale** e **apprendimento durante fit()**:

- scegliere `duration_ms` e `status_code`;
- scegliere Decision Tree;
- scegliere `max_depth=2`;
- scegliere una soglia come 205 ms;
- scegliere come combinare status e durata nei rami.

---

## Attività 7 — Test senza label

Perché `ml_test_features.csv` non contiene `reference_label`?

---

## Attività 8 — Precision e recall

Con:

```text
TP 7, FP 0, FN 2, TN 31
```

spiegare con parole proprie:

- precision = 1,00;
- recall ≈ 0,78.
