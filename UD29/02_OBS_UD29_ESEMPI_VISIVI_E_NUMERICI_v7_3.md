# UD29 — Esempi visivi e numerici

## Esempio 1 — Prima e dopo `fit()`

```text
PRIMA DI fit()

DecisionTreeClassifier(max_depth=2)
→ tipo di modello definito
→ nessuna regola ancora appresa dai nostri esempi

            ↓ fit(X, y)

DOPO fit()

duration_ms <= 205?
├── sì → controlla status_code
└── no → anomaly
```

La soglia non è stata programmata con un `if`.

### Nota sulla soglia di `status_code`

Se l'albero mostra:

```text
status_code <= 350?
```

non sta affermando una regola del protocollo HTTP. Sta separando numericamente gli esempi ricevuti.

```text
MODELLO VEDE                  DOMAIN EXPERT INTERPRETA
200, 300, 404, 500            successo, redirect, errori, contesto del servizio
      ↓                                      ↓
soglie apprese                significato operativo
```

La prediction deve quindi essere interpretata alla luce del dominio e delle evidenze disponibili.

---

## Esempio 2 — Stesso codice, dati diversi

### Dataset A

```text
150 normal
160 normal
170 normal
180 normal
230 anomaly
250 anomaly
165 + status 500 anomaly
```

Possibile soglia appresa:

```text
duration_ms <= 205
```

### Dataset B

```text
150 normal
160 normal
210 normal
220 normal
280 anomaly
300 anomaly
165 + status 500 anomaly
```

Possibile soglia appresa:

```text
duration_ms <= 250
```

Il codice è lo stesso. Sono cambiati gli esempi.

```text
DATI A → fit → MODELLO A
DATI B → fit → MODELLO B
```

---

## Esempio 3 — Learning e inference

```text
TRAINING
120 esempi + label
       ↓
      fit()
       ↓
   apprendimento
       ↓
     modello
```

```text
TEST
40 osservazioni senza label
       ↓
    predict()
       ↓
    inferenza
       ↓
   prediction
```

---

## Esempio 4 — Chi decide cosa

```text
NOI DECIDIAMO
├─ feature: duration_ms, status_code
├─ target: reference_label
├─ algoritmo: Decision Tree
└─ max_depth: 2

FIT APPRENDE DAI DATI
├─ quali separazioni usare
├─ quali soglie scegliere
└─ come combinare i rami
```

Questo evita due estremi sbagliati:

```text
"abbiamo scritto noi tutte le regole"       → falso
"il modello decide tutto spontaneamente"    → falso
```

---

## Esempio 5 — Prediction e reference

```text
test-017
duration/status
      ↓
   predict
      ↓
 prediction
```

Solo successivamente:

```text
prediction + reference di test-017
            ↓
          TP/FP/FN/TN
```

Il reference non viene usato per generare la prediction.
