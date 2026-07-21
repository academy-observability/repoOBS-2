# UD26 — Dal CSV al DataFrame

## Domanda guida

> Come rappresentiamo e leggiamo in memoria un'intera tabella di osservazioni?

Questa unità usa lo stesso file `mini_products_requests.csv` già incontrato durante il lavoro con `csv.DictReader`.

Il nuovo obiettivo non è imparare tutta la libreria pandas. Il nuovo obiettivo è capire il passaggio:

```text
riga CSV letta una alla volta
            ↓
tabella completa caricata in memoria
            ↓
DataFrame
```

## Ordine consigliato

1. `00_OBS_UD26_Concetti_Dataset_DataFrame_v7_0.md`
2. `02_OBS_UD26_ESEMPI_VISIVI_E_NUMERICI_v7_0.md`
3. `07_OBS_UD26_GUIDA_ARCHITETTURA_Dal_CSV_al_DataFrame_v7_0.md`
4. `05_OBS_UD26_GUIDA_OPERATIVA_Ambiente_Pandas_v7_0.md`
5. `01_OBS_UD26_LAB_guidato_Dal_CSV_al_DataFrame_v7_0.md`
6. `03_OBS_UD26_MINI_ATTIVITA_DataFrame_Filtri_v7_0.md`
7. `04_OBS_UD26_LAB_autonomo_Selezionare_Osservazioni_v7_0.md`
8. `06_OBS_UD26_Raccordo_Verso_Statistica_Descrittiva_v7_0.md`

## In questa UD impariamo

- che cos'è un dataset;
- che cosa rappresentano riga e colonna;
- che cos'è un DataFrame;
- come caricare un CSV con pandas;
- come osservare struttura e tipi;
- come selezionare una colonna;
- come filtrare righe con una condizione semplice.

## Non stiamo ancora facendo

- `groupby`;
- media, mediana e p95 come argomento didattico;
- baseline;
- anomaly detection;
- ground truth operativa;
- Machine Learning.
