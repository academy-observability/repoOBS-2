# Potenziamento 4 — Stabilità della baseline

## Livello
**Maggiore autonomia**

Tempo indicativo: **45–55 minuti**.

## Obiettivo
Verificare che una soglia dipende anche da **quali osservazioni scegliamo come baseline**.

## File
```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/04_baseline_stability_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/04_baseline_stability.py
```

## Scenario
Dal file di baseline costruire tre finestre:

```text
prime 20 osservazioni
prime 40 osservazioni
tutte le 60 osservazioni
```

Per ciascuna calcolare:

```text
median
MAD
threshold con multiplier = 4
numero di anomaly prediction su evaluation
```

## Output
```text
outputs/baseline_stability.csv
```

## Domande
1. Le tre soglie sono identiche?
2. Se cambiano, perché?
3. Più righe garantiscono automaticamente una baseline migliore?
4. Quale requisito resta più importante della sola numerosità?

Risposta chiave:

> La baseline deve rappresentare un contesto operativo coerente e realmente stabile; la numerosità da sola non basta.
