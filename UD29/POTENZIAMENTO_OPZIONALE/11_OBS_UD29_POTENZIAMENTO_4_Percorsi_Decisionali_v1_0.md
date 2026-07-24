# Potenziamento 4 — Leggere il percorso decisionale di singole osservazioni

## Livello

**Maggiore autonomia**

Tempo indicativo: **40–50 minuti**.

## Obiettivo

Non limitarsi a leggere l'albero in astratto. Seguire quattro osservazioni reali attraverso i rami del modello.

Casi suggeriti:

```text
test-002 → normal ordinario
test-010 → anomaly con status 500
test-006 → anomaly per durata elevata
test-016 → anomaly reale che il modello perde
```

## Starter

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/04_decision_paths_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/04_decision_paths.py
```

## Compiti

1. completare `CASE_IDS`;
2. eseguire lo script;
3. per ogni caso leggere:
   - feature;
   - condizioni attraversate;
   - prediction;
   - reference;
4. spiegare perché `test-016` segue coerentemente le regole apprese ma produce comunque una prediction sbagliata.

## Punto chiave

```text
percorso coerente con il modello
        ≠
prediction necessariamente corretta nel mondo reale
```

L'errore può dipendere dal fatto che l'evidenza necessaria non è rappresentata nelle feature disponibili.

## Codice di servizio

L'uso tecnico di `decision_path()` è già implementato. Non è richiesto imparare oggi l'API interna dell'albero: serve soltanto a rendere visibile il percorso.
