# UD28 — Esempi visivi e numerici

## Esempio 1 — Tre file, tre ruoli

Le dimensioni diverse sono intenzionali:

```text
baseline   60 osservazioni  ██████████████████████████████
evaluation 20 osservazioni  ██████████
reference  20 label         ██████████
```

Evaluation e reference sono 1:1. La baseline è più ampia perché costruisce il riferimento.

```text
TEMPO 08:00–09:58
baseline_products_requests.csv
        ↓
mediana + MAD
        ↓
soglia 196,5 ms

TEMPO 10:00–10:38
evaluation_products_requests.csv
        ↓
applico soglia
        ↓
prediction

VALIDAZIONE A POSTERIORI
products_reference_labels.csv
        ↓
stesse eval-001 ... eval-020
        ↓
reference label + reason + source
```

---

## Esempio 2 — Stessa observation_id, non nuova osservazione

```text
evaluation file

eval-005
10:08
190 ms
status 500
```

```text
reference file

eval-005
anomaly
unexpected_error
incident_review
```

Sono informazioni riferite alla stessa richiesta.

---

## Esempio 3 — Il falso negativo

```text
soglia = 196,5 ms
```

```text
eval-005
190 ms
status 500
```

Detector:

```text
190 < 196,5 → normal
```

Reference:

```text
anomaly
motivo: HTTP 500 inatteso
```

Risultato:

```text
FALSE NEGATIVE
```

---

## Esempio 4 — Il falso positivo

```text
eval-003
205 ms
status 200
```

Detector:

```text
205 > 196,5 → anomaly candidate
```

Reference:

```text
normal
motivo: picco transitorio di latenza accettato dal service owner per questo scenario
```

Risultato:

```text
FALSE POSITIVE
```

La soglia statistica è stata superata, ma il processo di validazione considera il comportamento previsto per quello scenario.

---

## Esempio 5 — Abbassare la soglia

Con moltiplicatore `4`:

```text
soglia = 196,5 ms
TP 4 / FP 2 / FN 1 / TN 13
precision ≈ 0,67
recall 0,80
```

Con moltiplicatore `3`:

```text
soglia = 189 ms
TP 5 / FP 3 / FN 0 / TN 12
precision = 0,625
recall = 1,00
```

Schema:

```text
soglia più bassa
     ↓
più casi segnalati
     ├── recupero l'anomaly eval-005
     └── segnalo anche eval-010, che la reference considera normal
```

Non esiste una soglia “migliore” in assoluto senza considerare il costo dei falsi positivi e dei falsi negativi.
