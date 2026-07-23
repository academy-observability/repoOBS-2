# Potenziamento 1 — Sensibilità della soglia

## Livello
**Guidato**

Tempo indicativo: **30–40 minuti**.

## Obiettivo
Osservare in modo sistematico che il moltiplicatore della formula:

```text
threshold = median + multiplier × MAD
```

non è neutro.

## File
Copiare:

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/01_threshold_sensitivity_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/01_threshold_sensitivity.py
```

## Compiti
1. completare la lista dei moltiplicatori `2, 3, 4, 5`;
2. per ciascuno calcolare la soglia;
3. applicarla alle observation di evaluation;
4. contare quante prediction `anomaly` vengono prodotte;
5. stampare una riga di riepilogo per ogni moltiplicatore.

## Modifica osservabile
Confrontare:

```text
moltiplicatore più basso
→ soglia più bassa
→ più casi segnalati

moltiplicatore più alto
→ soglia più alta
→ meno casi segnalati
```

## Domanda finale
Una soglia che segnala più casi è automaticamente migliore?

> No. Prima di giudicarla dobbiamo confrontare le prediction con una reference indipendente.
