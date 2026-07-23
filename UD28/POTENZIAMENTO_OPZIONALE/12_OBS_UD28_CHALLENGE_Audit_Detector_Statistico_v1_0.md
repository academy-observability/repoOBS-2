# Challenge finale — Audit di un detector statistico

## Livello
**Autonomo con codice di servizio fornito**

Tempo indicativo: **55–70 minuti**.

## Scenario
Un team Operations usa un detector molto semplice basato su `duration_ms` e chiede:

> Quanto è affidabile la regola? Come cambiano gli errori con soglie diverse? Quali casi dobbiamo discutere prima di adottarla operativamente?

## File
```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/05_detector_audit_CHALLENGE.py \
   POTENZIAMENTO_OPZIONALE/src/05_detector_audit.py
```

## Requisiti funzionali

### A. Confronto detector
Valutare almeno i moltiplicatori:

```text
2, 3, 4, 5
```

Produrre:

```text
outputs/audit_detector_comparison.csv
```

con:

```text
multiplier
threshold_ms
TP
FP
FN
TN
precision
recall
```

### B. Errori del detector scelto
Per `multiplier = 4` esportare:

```text
outputs/audit_error_cases.csv
```

contenente solo FP e FN.

### C. Stabilità baseline
Confrontare baseline da 20, 40 e 60 osservazioni e produrre:

```text
outputs/audit_baseline_stability.csv
```

### D. Conclusioni
Compilare:

```text
templates/conclusioni_challenge.md
```

con:
- 3 affermazioni supportate dai risultati;
- 2 limiti del detector;
- 1 rischio dei falsi positivi;
- 1 rischio dei falsi negativi;
- 2 evidenze aggiuntive utili prima di parlare di root cause.

## Vincolo
Il report può concludere:

> con questa baseline e questa soglia il detector produce...

Non può concludere automaticamente:

```text
questa è la soglia universale corretta
questa observation è sicuramente un incidente
questa è la root cause
serve Machine Learning
```
