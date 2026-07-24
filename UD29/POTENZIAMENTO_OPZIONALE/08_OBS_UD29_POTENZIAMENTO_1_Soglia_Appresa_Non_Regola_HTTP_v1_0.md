# Potenziamento 1 — Soglia appresa ≠ regola HTTP

## Livello

**Guidato**

Tempo indicativo: **30–40 minuti**.

## Obiettivo

Osservare come il Decision Tree si comporta su valori di `status_code` che non comparivano nel piccolo training set.

Il toy dataset contiene essenzialmente:

```text
200
500
```

e l'albero può apprendere:

```text
status_code <= 350?
```

Vogliamo verificare concretamente che questa è una **soglia numerica appresa**, non una regola HTTP.

## Starter

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/01_probe_unseen_status_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/01_probe_unseen_status.py
```

## Compiti

1. completare `PROBE_STATUS_CODES` con `200`, `300`, `404`, `500`;
2. mantenere per tutti i casi `duration_ms = 170`;
3. eseguire il modello addestrato sul toy dataset;
4. leggere le prediction;
5. spiegare perché `300` e `404` vengono separati dal ramo appreso pur non essendo presenti nel training.

## Risultato da interpretare

Con il toy model attuale ci aspettiamo:

```text
170 / 200 → normal
170 / 300 → normal
170 / 404 → anomaly
170 / 500 → anomaly
```

La domanda importante non è:

> “Il modello ha imparato correttamente HTTP?”

ma:

> “Quale separazione numerica ha imparato dagli esempi?”

## Vincolo interpretativo

Non concludere:

```text
<= 350 = sempre corretto
> 350  = sempre errore
```

Il significato operativo dipende dal protocollo, dal contratto dell'endpoint e dal contesto del servizio.
