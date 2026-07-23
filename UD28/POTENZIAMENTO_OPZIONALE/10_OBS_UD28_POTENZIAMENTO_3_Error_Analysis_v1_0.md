# Potenziamento 3 — Analizzare falsi positivi e falsi negativi

## Livello
**Specifiche + struttura minima**

Tempo indicativo: **40–50 minuti**.

## Obiettivo
Passare dai soli conteggi aggregati ai casi concreti che producono errore.

## File
```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/03_error_analysis_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/03_error_analysis.py
```

## Compiti
Usando il detector con `multiplier = 4`:

1. produrre prediction;
2. unire prediction e reference per `observation_id`;
3. classificare ogni riga come TP, FP, FN o TN;
4. filtrare soltanto FP e FN;
5. esportare:

```text
outputs/error_cases.csv
```

Le colonne minime:

```text
observation_id
duration_ms
status_code
predicted_label
reference_label
outcome
reference_reason_code
reference_reason
label_source
```

## Vincolo interpretativo
Per ogni errore distinguere:

```text
perché il detector ha deciso così
≠
perché la reference considera il caso normal/anomaly
≠
root cause tecnica
```

## Domanda finale
Che cosa dimostra `eval-005`?

> Che un detector basato soltanto su `duration_ms` può perdere un'anomalia riconosciuta da evidenze che il detector non osserva.
