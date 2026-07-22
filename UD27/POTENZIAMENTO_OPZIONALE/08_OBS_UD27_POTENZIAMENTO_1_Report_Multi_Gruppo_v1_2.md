# Potenziamento 1 — Report statistico multi-gruppo

## Livello

**Guidato**

Tempo di lavoro indicativo: **30–40 minuti**.

## Obiettivo

Applicare la stessa analisi statistica a più gruppi senza duplicare il codice.

Copiare:

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/01_multi_group_report_TODO.py \
   POTENZIAMENTO_OPZIONALE/src/01_multi_group_report.py
```

---

## Prima di eseguire

Lo script contiene una funzione:

```python
describe_group(...)
```

che riceve:

```text
dataset
service
endpoint
```

e restituisce:

```text
count
min
max
mean
median
p95
```

Il codice che trova il dataset e costruisce il `DataFrame` finale è già fornito come **codice di servizio**.

Il partecipante deve concentrarsi su:

```text
filtro
statistiche
riuso della funzione
```

---

## Compiti

1. completare `median`;
2. completare `p95`;
3. completare la lista dei quattro gruppi;
4. completare il ciclo che richiama la funzione;
5. eseguire lo script;
6. verificare che il report contenga 4 righe.

---

## Modifica osservabile

Rimuovere temporaneamente i due gruppi `/slow`.

Eseguire di nuovo.

Domanda:

> Quale parte del risultato cambia? Le statistiche dei gruppi rimasti vengono ricalcolate diversamente?

Ripristinare infine i quattro gruppi.
