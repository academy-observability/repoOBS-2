# Potenziamento 3 — Correlare richieste a partire da una lista di ID

## Livello

**Specifiche + struttura minima**

Tempo di lavoro indicativo: **40–50 minuti**.

## Obiettivo

Costruire uno script che analizzi più `request_id` e produca per ciascuno:

```text
numero righe trovate
trace_id
servizi coinvolti
status_code
durata minima
durata massima
differenza max-min
```

---

## Input già fornito

```python
request_ids = [
    "req-0067",
    "req-0132",
    "req-0158",
    "req-0005",
]
```

Il quarto caso è importante:

> lo script non deve assumere che ogni request abbia sempre esattamente due righe.

---

## Compiti

Per ogni `request_id`:

1. filtrare il DataFrame;
2. gestire il caso senza righe;
3. costruire un riepilogo;
4. aggiungerlo alla lista `results`.

Il codice che:

- trova il dataset;
- converte `results` in DataFrame;
- esporta il CSV;

è già fornito e commentato come **codice di servizio**.

---

## Output

Creare:

```text
POTENZIAMENTO_OPZIONALE/outputs/request_correlation_summary.csv
```

---

## Vincolo interpretativo

La differenza:

```text
max(duration_ms) - min(duration_ms)
```

è soltanto una differenza numerica.

Non chiamarla automaticamente:

```text
latenza di rete
overhead frontend
root cause
```
