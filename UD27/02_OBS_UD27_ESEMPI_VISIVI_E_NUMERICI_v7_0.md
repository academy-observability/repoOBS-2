# UD27 — Esempi visivi e numerici

Questo file raccoglie esempi piccoli da comprendere **prima** di usare il dataset completo del laboratorio.

---

# Esempio 1 — Media e mediana

Valori:

```text
100   105   110   115   900
```

## Media

```text
(100 + 105 + 110 + 115 + 900) / 5 = 266
```

## Mediana

```text
100   105   [110]   115   900
             ↑
          valore centrale
```

```text
mediana = 110
```

## Immagine mentale

```text
100  105  110  115                                      900
●----●----●----●------------------------------------------●
          ↑                       ↑
       mediana                  media spostata
```

### Idea da fissare

Il valore `900` influenza molto la media.

La differenza tra media e mediana ci aiuta a vedere che la distribuzione non è equilibrata attorno a un unico gruppo di valori simili.

---

# Esempio 2 — Perché separare i gruppi

Supponiamo di avere:

```text
/products       100  110  120  130
/products/slow  700  750  800  850
```

Se mescoliamo tutto:

```text
100 110 120 130 700 750 800 850
```

la media complessiva non rappresenta bene né l'endpoint normale né quello slow.

```text
          un'unica media globale
                  ↓
/products      --------
/products/slow ------------------------------
```

Meglio descrivere separatamente:

```text
GRUPPO 1                    GRUPPO 2
/products                   /products/slow
100 110 120 130             700 750 800 850
```

### Idea da fissare

> Un numero è utile soltanto se sappiamo quale insieme di osservazioni sta riassumendo.

---

# Esempio 3 — Che cosa fa `groupby`

Prima, manualmente:

```text
Filtro 1 → frontend + /products
Filtro 2 → backend  + /api/products
Filtro 3 → frontend + /products/slow
Filtro 4 → backend  + /api/products/slow
```

Con `groupby`:

```text
                 DataFrame
                    │
          groupby(service, endpoint)
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       gruppo 1  gruppo 2  gruppo 3 ...
          │         │         │
       media      media      media
```

`groupby` non decide quali gruppi siano buoni o cattivi.

Li separa e ci permette di applicare lo stesso calcolo a ciascuno.

---

# Esempio 4 — p95 senza partire dalla formula

Usiamo 21 valori già ordinati:

```text
100 101 102 103 104 105 106 107 108 109
110 111 112 113 114 115 116 117 118 119 500
```

Visualmente:

```text
100 ........................................ 119 | 500
└──────────── circa il 95% dei valori ─────────┘   ↑
                                                   massimo
```

Con questa serie, il p95 è `119`.

Il valore massimo è invece `500`.

### Idea da fissare

```text
p95 ≠ massimo
```

Il p95 descrive la zona in cui ricade quasi tutta la distribuzione lasciando fuori la parte più estrema.

---

# Esempio 5 — Tabella e tempo

Supponiamo che cinque richieste abbiano durate:

```text
100, 110, 500, 120, 130
```

Una tabella può dirci:

```text
media = 192
mediana = 120
massimo = 500
```

Ma solo mantenendo il tempo vediamo **quando** è comparso il valore 500:

```text
08:00  100
08:01  110
08:02  500  ← valore alto
08:03  120
08:04  130
```

```text
durata
  ↑
500|        ●
400|
300|
200|
100| ●  ●      ●  ●
   +----------------→ tempo
```

### Idea da fissare

- le statistiche **riassumono**;
- il grafico temporale conserva **l'ordine nel tempo**.

---

# Tre frasi da saper completare

1. La media può essere influenzata da...
2. `groupby` serve a...
3. Il p95 non deve essere confuso con...
