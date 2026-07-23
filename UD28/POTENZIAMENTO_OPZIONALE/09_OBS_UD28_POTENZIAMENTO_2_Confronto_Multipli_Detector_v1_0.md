# Potenziamento 2 — Confrontare più detector statistici

## Livello
**Parzialmente guidato**

Tempo indicativo: **35–45 minuti**.

## Obiettivo
Costruire una funzione che valuti più valori di `multiplier` e restituisca per ciascuno:

```text
threshold
TP
FP
FN
TN
precision
recall
```

## File
```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/02_compare_detectors_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/02_compare_detectors.py
```

## Requisito principale
Creare:

```python
evaluate_detector(multiplier)
```

La funzione deve:
1. costruire la soglia;
2. produrre prediction senza leggere prima la reference;
3. associare successivamente le reference label;
4. calcolare TP, FP, FN, TN;
5. calcolare precision e recall;
6. restituire un dizionario.

## Output
Creare:

```text
POTENZIAMENTO_OPZIONALE/outputs/detector_comparison.csv
```

## Domanda finale
Esiste un moltiplicatore “migliore in assoluto”?

> No. Il risultato dipende dall'obiettivo operativo e dal costo relativo di falsi positivi e falsi negativi.
