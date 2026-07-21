# UD26 — Esempi visivi
# Dataset, DataFrame, colonne e filtri

## 1. Una tabella piccola prima del codice

| riga | service | endpoint | status_code | duration_ms |
|---:|---|---|---:|---:|
| 1 | frontend | /products | 200 | 110 |
| 2 | backend | /api/products | 200 | 85 |
| 3 | frontend | /products | 200 | 130 |
| 4 | backend | /api/products | 500 | 95 |
| 5 | frontend | /products/slow | 200 | 750 |

### Domande

- Quante osservazioni vediamo? **5**.
- Quante proprietà mostriamo? **4**.
- Quante righe appartengono al frontend? **3**.
- Quante righe hanno status 5xx? **1**.

Queste domande sono le stesse che poi faremo al DataFrame.

---

## 2. Da CSV a DataFrame

```text
FILE CSV

service,endpoint,status_code,duration_ms
frontend,/products,200,110
backend,/api/products,200,85
...

          │ pd.read_csv()
          ▼

DATAFRAME IN MEMORIA

┌──────────┬───────────────┬─────────────┬─────────────┐
│ service  │ endpoint      │ status_code │ duration_ms │
├──────────┼───────────────┼─────────────┼─────────────┤
│ frontend │ /products     │ 200         │ 110         │
│ backend  │ /api/products │ 200         │ 85          │
└──────────┴───────────────┴─────────────┴─────────────┘
```

Il contenuto rappresentato è lo stesso. Cambia il modo in cui Python lo gestisce.

---

## 3. Selezionare una colonna

```text
DataFrame

service     duration_ms
frontend    110
backend      85
frontend    130
backend      95
frontend    750
              │
              │ data["duration_ms"]
              ▼
            110
             85
            130
             95
            750
```

Selezionare non significa calcolare.

Stiamo soltanto indicando quale proprietà vogliamo osservare.

---

## 4. Come funziona un filtro

Condizione:

```python
data["service"] == "frontend"
```

Concettualmente:

| service | è frontend? |
|---|---|
| frontend | True |
| backend | False |
| frontend | True |
| backend | False |
| frontend | True |

Il filtro conserva le righe associate a `True`:

| service | endpoint | status_code | duration_ms |
|---|---|---:|---:|
| frontend | /products | 200 | 110 |
| frontend | /products | 200 | 130 |
| frontend | /products/slow | 200 | 750 |

---

## 5. Che cosa cambia e che cosa non cambia

Quando passiamo dal filtro frontend al filtro backend:

```text
CAMBIA
- quali righe vediamo
- quanti record possono essere presenti

NON CAMBIA
- il file CSV originale
- i nomi delle colonne
- il significato delle colonne
```

---

## 6. Un errore concettuale da evitare

Vedere una durata alta:

```text
750 ms
```

non ci autorizza ancora a dire:

```text
anomalia
incidente
root cause
```

In UD26 stiamo imparando a leggere e selezionare i dati.

L'interpretazione statistica arriverà dopo.
