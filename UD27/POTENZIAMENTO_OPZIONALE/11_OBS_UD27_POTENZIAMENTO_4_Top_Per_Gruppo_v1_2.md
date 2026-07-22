# Potenziamento 4 — Top richieste per ogni gruppo

## Livello

**Maggiore autonomia**

Tempo di lavoro indicativo: **40–50 minuti**.

## Obiettivo

Per ogni gruppo principale:

```text
frontend /products
backend  /api/products
```

mostrare automaticamente le **3 osservazioni con duration_ms più alta**.

---

## Requisiti

Il programma deve:

1. ricevere la lista dei gruppi;
2. filtrare ciascun gruppo;
3. ordinare per `duration_ms` decrescente;
4. prendere le prime `top_n`;
5. aggiungere una colonna `rank` con valori `1, 2, 3`;
6. produrre un unico DataFrame finale;
7. esportare:

```text
outputs/top_observations_by_group.csv
```

---

## Codice di servizio

Sono già forniti:

- caricamento dataset;
- funzione `take_top_rows()` che ordina e prende le prime N righe;
- esportazione CSV.

Perché?

> L'obiettivo non è imparare oggi la sintassi dettagliata di `sort_values`, `head` o `concat`, ma progettare il flusso che applica la stessa analisi a più gruppi.

Il partecipante deve completare soprattutto:

```text
lista gruppi
ciclo
filtri
rank
lista dei risultati
```

---

## Modifica

Dopo aver ottenuto il risultato con:

```python
top_n = 3
```

provare:

```python
top_n = 2
```

e poi:

```python
top_n = 5
```

Spiegare che cosa cambia e che cosa rimane invariato.
