# UD26 — Laboratorio autonomo
# Selezionare osservazioni

## Scenario

Abbiamo ricevuto il mini dataset delle richieste del Catalogo prodotti.

Dobbiamo produrre tre viste semplici:

1. osservazioni frontend;
2. osservazioni backend;
3. osservazioni con status 5xx.

Non dobbiamo ancora calcolare statistiche o classificare anomalie.

---

## Preparazione

Copiare lo starter:

Linux / WSL:

```bash
cp src/starter/select_observations_TODO.py src/select_observations.py
```

PowerShell:

```powershell
Copy-Item src/starter/select_observations_TODO.py src/select_observations.py
```

Preparare anche il file delle evidenze.

Linux / WSL:

```bash
cp templates/evidence_ud26_template.md evidence/evidence_ud26.md
```

PowerShell:

```powershell
Copy-Item templates/evidence_ud26_template.md evidence/evidence_ud26.md
```

---

## Compito

Completare soltanto i quattro TODO.

Sono consentite le operazioni già viste:

```python
pd.read_csv(...)
data["colonna"]
data[condizione]
len(...)
.head(2)
```

## Output richiesto

Per ciascun sottoinsieme stampare:

- numero di righe;
- prime due righe.

## Evidenza

Compilare:

```text
evidence/evidence_ud26.md
```

spiegando:

1. che cosa contiene `data`;
2. quale condizione hai usato per frontend;
3. quale condizione hai usato per 5xx;
4. perché il CSV originale non è stato modificato;
5. quale differenza c'è tra selezionare una colonna e filtrare righe.

## Vincoli

Non usare:

- `groupby`;
- `mean`;
- `median`;
- `quantile`;
- soglie;
- Machine Learning.

Questi argomenti appartengono alle unità successive.
