# UD27 — Mini-attività
# Statistiche e gruppi

Le attività servono a consolidare concetti già introdotti. Non aggiungono nuove API.

---

## Attività 1 — Media o mediana?

Valori:

```text
90, 95, 100, 105, 610
```

Senza usare Python:

1. individuare la mediana;
2. prevedere se la media sarà maggiore o minore della mediana;
3. spiegare quale valore influenza maggiormente la media.

---

## Attività 2 — Quale gruppo?

Abbiamo due gruppi:

```text
A: frontend /products
B: frontend /products/slow
```

Spiegare perché una media ottenuta mescolando A e B è meno utile delle due medie separate.

---

## Attività 3 — Leggere `groupby`

Spiegare con parole proprie:

```python
groups = data.groupby(["service", "endpoint"])["duration_ms"]
```

Usare la forma:

```text
prende...
separa...
considera...
```

---

## Attività 4 — p95 e massimo

Valori ordinati:

```text
100 101 102 103 104 105 106 107 108 109
110 111 112 113 114 115 116 117 118 119 500
```

Rispondere:

1. il massimo è?
2. il p95 dell'esempio è?
3. perché non coincidono?
4. possiamo concludere che `500` sia un incidente?

---

## Attività 5 — Tabella o grafico?

Associare la domanda allo strumento più adatto:

### Domanda A

> Qual è la mediana delle durate del gruppo?

### Domanda B

> In quale momento compare il valore più alto?

Scegliere tra:

```text
tabella statistica
grafico temporale
```

e motivare.
