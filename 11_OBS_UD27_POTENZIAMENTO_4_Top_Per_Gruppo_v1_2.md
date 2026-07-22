# Potenziamento 2 — Costruire una funzione di confronto

## Livello

**Parzialmente guidato**

Tempo di lavoro indicativo: **35–45 minuti**.

## Obiettivo

Costruire una funzione che confronti due gruppi usando:

```text
mean
median
p95
```

Lo starter fornisce soltanto:

- caricamento dataset;
- funzione di servizio per selezionare un gruppo;
- stampa finale.

Il partecipante deve progettare la parte centrale.

---

## Requisito

Creare:

```python
compare_groups(...)
```

che riceva:

```text
data
service_a
endpoint_a
service_b
endpoint_b
```

e produca un dizionario con:

```text
mean_a
mean_b
mean_difference

median_a
median_b
median_difference

p95_a
p95_b
p95_difference
```

Le differenze devono essere:

```text
gruppo A - gruppo B
```

---

## Caso da analizzare

```text
A = frontend /products
B = backend  /api/products
```

---

## Verifica finale

Il programma deve mostrare che le differenze tra:

```text
mean
median
p95
```

non sono identiche.

Domanda finale:

> Perché confrontare soltanto una statistica può fornire una descrizione incompleta?
