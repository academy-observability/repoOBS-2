# UD28 — Guida architetturale
# Dati, detector e reference

```mermaid
flowchart LR
    B[Baseline observations<br/>base-*] --> S[Mediana + MAD<br/>Soglia]
    S --> D[Detector]
    E[Evaluation observations<br/>eval-*] --> D
    D --> P[Prediction]
    R[Reference labels<br/>stesse eval-*] --> C[Confronto]
    P --> C
    C --> M[TP FP FN TN<br/>Precision Recall]
```

## Relazioni corrette

### Baseline ↔ Evaluation

Sono **osservazioni differenti**, raccolte in periodi differenti.

Non vengono confrontate riga per riga.

La baseline produce un riferimento statistico che viene applicato alle evaluation observations.

### Evaluation ↔ Reference

Sono informazioni sulla **stessa observation_id**.

```text
eval-005 dati osservati
↔
eval-005 classificazione di riferimento
```

Il reference file non rappresenta un nuovo evento.

## Processo reale di labeling

```text
SRE / Operations
+ Service Owner
+ QA / controlled tests
+ incident review
+ evidenze log/trace
        ↓
validazione
        ↓
label di riferimento
```

Il CSV del laboratorio rappresenta il risultato finale di questo processo.
