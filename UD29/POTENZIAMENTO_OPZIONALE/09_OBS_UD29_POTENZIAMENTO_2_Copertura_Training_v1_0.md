# Potenziamento 2 — Quanto conta la copertura del training?

## Livello

**Parzialmente guidato**

Tempo indicativo: **35–45 minuti**.

## Obiettivo

Confrontare lo stesso Decision Tree in due condizioni:

```text
MODELLO A
training completo

MODELLO B
training senza esempi status_code = 500
```

Non cambiano algoritmo, feature, `max_depth` o test set.

## Starter

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/02_training_coverage_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/02_training_coverage.py
```

## Compiti

1. costruire `training_without_500`;
2. addestrare e valutare i due modelli tramite la funzione fornita;
3. confrontare le regole apprese;
4. confrontare TP, FP, FN, TN, precision e recall;
5. individuare quali casi il modello B non riconosce più.

## Domande

1. Il modello B può apprendere bene un ramo dedicato a `500` se non ne ha mai visto alcun esempio?
2. La feature `status_code` continua a esistere nel modello B: perché questo non basta?
3. Che differenza c'è tra **avere una feature** e **avere esempi sufficienti per apprendere come usarla**?

## Messaggio chiave

```text
feature disponibile
        +
training rappresentativo
        ↓
apprendimento utile
```

La sola presenza di una colonna non garantisce che il modello possa apprendere tutti i comportamenti rilevanti.
