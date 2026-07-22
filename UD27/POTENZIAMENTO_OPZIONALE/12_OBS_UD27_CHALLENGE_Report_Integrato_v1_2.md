# Challenge finale — Report integrato di Observability descrittiva

## Livello

**Autonomo con codice di servizio fornito**

Tempo di lavoro indicativo: **55–70 minuti**.

## Scenario

Un collega chiede:

> Puoi produrre un riepilogo automatico dei dati del Catalogo prodotti, confrontare frontend e backend e indicare alcune richieste da approfondire, senza dichiarare anomalie o root cause non dimostrate?

---

# File

Copiare:

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/05_integrated_report_CHALLENGE.py \
   POTENZIAMENTO_OPZIONALE/src/05_integrated_report.py
```

---

# Requisiti funzionali

Lo script deve produrre:

## A. `group_summary.csv`

Per:

```text
frontend /products
backend  /api/products
```

con:

```text
count
mean
median
p95
max
```

## B. `top_requests.csv`

Le prime 3 richieste per `duration_ms` di ciascun gruppo.

## C. Output console

Mostrare:

```text
differenza mean frontend-backend
differenza median frontend-backend
differenza p95 frontend-backend
```

## D. Conclusioni

Compilare:

```text
templates/conclusioni_challenge.md
```

con:

- 3 affermazioni supportate;
- 2 limiti dell'analisi;
- 2 domande da approfondire.

---

# Cosa è già fornito

Nello starter sono già presenti e commentati come **codice di servizio**:

- percorsi input/output;
- lettura CSV;
- creazione directory output;
- funzione di esportazione CSV;
- funzione tecnica per ordinare e prendere le top N.

Questi blocchi non devono essere reinventati.

---

# Cosa deve progettare il partecipante

- funzione `describe_group`;
- lista dei gruppi;
- ciclo di costruzione del riepilogo;
- differenze tra statistiche;
- ciclo per le top richieste;
- costruzione del rank;
- scelta delle colonne finali.

---

# Vincolo

Il report può dire:

> Nel campione osservato...

Non può concludere automaticamente:

```text
anomalia
incidente
root cause
```

perché questi concetti richiedono evidenze ulteriori.
