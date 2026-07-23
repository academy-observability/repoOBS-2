# UD28 — Laboratorio autonomo
# Valutare una soglia alternativa

## Obiettivo

Confrontare il detector con:

```text
moltiplicatore = 4
moltiplicatore = 3
```

senza introdurre nuove tecniche.

## Starter

```bash
cp src/starter/evaluate_threshold_TODO.py src/evaluate_threshold.py
```

PowerShell:

```powershell
Copy-Item src/starter/evaluate_threshold_TODO.py src/evaluate_threshold.py
```

## TODO

1. calcolare mediana e MAD dalla baseline;
2. costruire la soglia con il moltiplicatore assegnato;
3. applicarla al file evaluation;
4. confrontare con il reference file;
5. calcolare TP, FP, FN, TN;
6. calcolare precision e recall.

## Evidenza

| Moltiplicatore | Soglia | TP | FP | FN | TN | Precision | Recall |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | | | | | | | |
| 3 | | | | | | | |

## Domanda finale

Quale soglia sceglieresti se fosse molto costoso perdere un'anomalia?

La risposta deve discutere anche l'aumento dei falsi positivi.
