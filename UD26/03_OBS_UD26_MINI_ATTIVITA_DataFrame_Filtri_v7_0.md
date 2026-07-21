# UD26 — Mini-attività
# DataFrame, colonne e filtri

Le attività servono a consolidare concetti già visti. Non introducono nuove API.

## Attività 1 — CSV o DataFrame?

Associare ogni frase:

1. È un file salvato sul disco.
2. È una tabella caricata in memoria.
3. Viene creato con `pd.read_csv()`.
4. Può esistere anche quando Python non è in esecuzione.

Categorie:

```text
CSV
DataFrame
```

---

## Attività 2 — Riga o colonna?

Per ciascun elemento indicare se descrive:

- una proprietà;
- una osservazione.

```text
status_code
obs-000263, ..., backend, /api/products, 500, 181.71, ...
duration_ms
service
```

---

## Attività 3 — Prevedere il filtro

Data:

| service | status_code |
|---|---:|
| frontend | 200 |
| backend | 200 |
| frontend | 500 |
| backend | 200 |

Condizione:

```python
data["service"] == "frontend"
```

Scrivere la sequenza True/False prevista.

---

## Attività 4 — Spiegare con parole proprie

Spiegare:

```python
selected_rows = data[data["status_code"] >= 500]
```

senza usare la frase “perché funziona così in pandas”.

---

## Attività 5 — Cosa possiamo concludere?

Abbiamo filtrato due righe con status 500.

Quali frasi sono corrette?

- A. Abbiamo osservato due risposte 5xx.
- B. Abbiamo dimostrato che il backend è la root cause.
- C. Abbiamo creato un sottoinsieme delle osservazioni.
- D. Abbiamo modificato il CSV originale.

Motivare.
