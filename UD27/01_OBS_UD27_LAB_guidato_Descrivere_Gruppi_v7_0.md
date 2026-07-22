# UD27 — Laboratorio guidato
# Descrivere e confrontare gruppi di osservazioni

## Obiettivo

Alla fine del laboratorio dovremo saper spiegare questa progressione:

```text
DataFrame
   ↓
seleziono le durate
   ↓
calcolo statistiche
   ↓
separo gruppi confrontabili
   ↓
uso groupby per automatizzare
   ↓
leggo il p95
   ↓
osservo il tempo con un grafico
```

Non basta eseguire gli script. Prima di ogni comando:

1. leggiamo il codice;
2. prevediamo il risultato;
3. eseguiamo;
4. interpretiamo;
5. modifichiamo qualcosa di osservabile.

---

# Task 1 — Riprendere ciò che sappiamo da UD26

Aprire:

```text
datasets/mini_products_requests.csv
```

Rispondere senza eseguire codice:

1. Quante righe contiene?
2. Quale colonna contiene la durata?
3. Come selezioneremmo soltanto il frontend?
4. Che cosa rappresenta una singola riga?

### Obiettivo del richiamo

UD27 non parte da zero: riutilizza DataFrame, colonne e filtri già esercitati.

---

# Task 2 — Capire media e mediana prima del codice

Usare questi valori:

```text
100   105   110   115   900
```

Calcolare insieme:

```text
count   = 5
min     = 100
max     = 900
media   = 266
mediana = 110
```

## Domanda

Perché la media `266` è molto più alta di quasi tutti i primi quattro valori?

### Idea da fissare

Il valore `900` influenza la media molto più della mediana.

Non stiamo ancora parlando di anomalia: stiamo osservando la forma dei valori.

---

# Task 3 — Calcolare statistiche sul dataset

## File

```text
src/01_basic_statistics.py
```

## Prima dell'esecuzione: leggiamo il codice

### Blocco 1 — Codice già conosciuto

```python
data = pd.read_csv(DATASET_PATH)
```

È lo stesso passaggio di UD26: CSV → DataFrame.

### Blocco 2 — Selezione della colonna

```python
durations = data["duration_ms"]
```

Abbiamo già imparato a selezionare una colonna.

### Blocco 3 — Nuovo concetto

```python
print("Count:", durations.count())
print("Minimo:", durations.min())
print("Massimo:", durations.max())
print("Media:", round(durations.mean(), 2))
print("Mediana:", round(durations.median(), 2))
```

Leggiamo le operazioni:

```text
count()  → quanti valori
min()    → valore più piccolo
max()    → valore più grande
mean()   → media
median() → mediana
```

## Previsione

Prima di eseguire:

- `count` sarà 20?
- il massimo sarà vicino alle normali richieste o agli endpoint slow?
- media e mediana saranno uguali?

## Esecuzione

```bash
python src/01_basic_statistics.py
```

## Modifica guidata

### Cercare

```python
# MODIFICA GUIDATA - TASK 3
```

### Codice iniziale

```python
durations = data["duration_ms"]
```

### Sostituire temporaneamente con

```python
durations = data["duration_ms"].head(5)
```

### Previsione

Ora stiamo descrivendo soltanto le prime cinque durate.

Che cosa cambierà?

- count;
- minimo/massimo;
- media;
- mediana.

### Esecuzione

```bash
python src/01_basic_statistics.py
```

### Domanda

Perché le statistiche cambiano quando cambia l'insieme di osservazioni che stiamo descrivendo?

### Ripristino

```python
durations = data["duration_ms"]
```

---

# Task 4 — Descrivere un gruppo preciso

## File

```text
src/02_statistics_one_group.py
```

## Passo 1 — Filtro già conosciuto

```python
selected = data[
    (data["service"] == "frontend")
    & (data["endpoint"] == "/products")
]
```

Questa parte riutilizza UD26.

La novità non è il filtro.

La novità è calcolare le statistiche **dopo** aver scelto un gruppo coerente.

## Passo 2 — Statistiche del gruppo

```python
durations = selected["duration_ms"]
```

Poi calcoliamo count, minimo, massimo, media e mediana.

## Previsione

Guardando il CSV:

- quante righe appartengono a `frontend /products`?
- il massimo sarà ancora `1586.79 ms`?

Motivare la risposta.

## Esecuzione

```bash
python src/02_statistics_one_group.py
```

## Modifica guidata

### Cercare

```python
# MODIFICA GUIDATA - TASK 4
```

### Cambiare il gruppo

Da:

```python
service = "frontend"
endpoint = "/products"
```

A:

```python
service = "backend"
endpoint = "/api/products"
```

## Previsione

Il numero di righe resterà uguale, ma le statistiche cambieranno.

## Domanda

Perché è più corretto confrontare:

```text
frontend /products
con
backend /api/products
```

separatamente, invece di mescolare anche gli endpoint `/slow`?

---

# Task 5 — Dal filtro manuale a `groupby`

## File

```text
src/03_group_data.py
```

Prima di leggere il codice, immaginiamo di voler ripetere:

```text
seleziona gruppo
→ calcola count
→ calcola media
→ calcola mediana
```

per tutti i gruppi.

Scrivere molti filtri sarebbe ripetitivo.

## Codice centrale

```python
groups = data.groupby(["service", "endpoint"])["duration_ms"]
```

Leggiamolo:

```text
data
→ raggruppa per service ed endpoint
→ per ogni gruppo considera duration_ms
```

Poi:

```python
print(groups.count())
print(groups.mean().round(2))
print(groups.median().round(2))
```

## Esecuzione

```bash
python src/03_group_data.py
```

## Confronto con Task 4

Individuare nella tabella il gruppo:

```text
frontend /products
```

I valori di media e mediana devono corrispondere a quelli calcolati manualmente nello script precedente.

### Questa verifica è importante

`groupby` non sta facendo qualcosa di misterioso.

Sta ripetendo automaticamente lo stesso ragionamento per tutti i gruppi.

## Modifica guidata

### Codice iniziale

```python
groups = data.groupby(["service", "endpoint"])["duration_ms"]
```

### Sostituire temporaneamente con

```python
groups = data.groupby(["service"])["duration_ms"]
```

## Domanda

Perché ora vediamo soltanto due gruppi?

Che cosa abbiamo perso eliminando `endpoint` dalla chiave di raggruppamento?

### Ripristino

Ripristinare:

```python
groups = data.groupby(["service", "endpoint"])["duration_ms"]
```

---

# Task 6 — Comprendere il p95 prima del codice

Aprire:

```text
02_OBS_UD27_ESEMPI_VISIVI_E_NUMERICI_v7_0.md
```

Usare i 21 valori dell'esempio.

Fissare questa distinzione:

```text
p95 = 119
massimo = 500
```

## Domanda

Perché p95 e massimo non coincidono?

### Idea da fissare

Il massimo descrive il caso più estremo.

Il p95 descrive il limite sotto il quale ricade circa il 95% delle osservazioni.

---

# Task 7 — Calcolare il p95 di un gruppo reale

## File

```text
src/04_calculate_p95.py
```

## Codice centrale

```python
p95 = durations.quantile(0.95)
```

`0.95` rappresenta il 95% espresso come numero tra 0 e 1.

## Esecuzione

```bash
python src/04_calculate_p95.py
```

Lo script mostra:

- count;
- mediana;
- p95;
- massimo.

## Domanda

Che cosa raccontano di diverso:

```text
mediana
p95
massimo
```

## Modifica guidata

Cambiare:

```python
service = "frontend"
endpoint = "/products"
```

in:

```python
service = "backend"
endpoint = "/api/products"
```

Confrontare i due p95.

### Attenzione

Non scrivere:

> Il gruppo con p95 maggiore è anomalo.

Possiamo soltanto dire:

> Nel dataset osservato, quel gruppo presenta una parte lenta della distribuzione più elevata.

---

# Task 8 — Conservare la dimensione temporale

## File

```text
src/05_plot_one_group.py
```

## Codice da comprendere

Il filtro:

```python
selected = data[
    (data["service"] == "frontend")
    & (data["endpoint"] == "/products")
].copy()
```

è già noto.

Convertiamo poi il timestamp:

```python
selected["timestamp_utc"] = pd.to_datetime(selected["timestamp_utc"])
```

Questo permette al grafico di trattare la colonna come tempo.

## Codice di servizio

La configurazione di matplotlib serve soltanto a creare il PNG.

Non è richiesto ricordarne tutta la sintassi.

## Esecuzione

```bash
python src/05_plot_one_group.py
```

Aprire:

```text
outputs/frontend_products_duration.png
```

## Domanda

Quale informazione vediamo nel grafico che una sola media non può mostrarci?

## Modifica guidata

Cambiare il filtro in:

```python
service = "backend"
endpoint = "/api/products"
```

Cambiare anche il nome dell'output in:

```text
backend_api_products_duration.png
```

Confrontare i due grafici.

---

# Task 9 — Compilare l'evidenza

Copiare:

```bash
cp templates/evidence_ud27_template.md evidence/evidence_ud27.md
```

PowerShell:

```powershell
Copy-Item templates/evidence_ud27_template.md evidence/evidence_ud27.md
```

Completare senza usare parole come `anomalia`, `incidente` o `root cause` se non per spiegare che **non possiamo ancora concluderle**.

---

# Criterio di completamento

Il laboratorio è completato quando sappiamo spiegare:

1. differenza tra media e mediana;
2. perché separare i gruppi;
3. che cosa automatizza `groupby`;
4. che cosa descrive il p95;
5. che cosa aggiunge il grafico temporale;
6. perché nessuna di queste statistiche, da sola, conferma un'anomalia.
