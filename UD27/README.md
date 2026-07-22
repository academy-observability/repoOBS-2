# UD27 — Descrivere il comportamento dei dati

## Domanda guida

> Come descriviamo numericamente il comportamento di gruppi diversi di osservazioni?

In UD26 abbiamo imparato a:

```text
caricare un CSV
      ↓
DataFrame
      ↓
selezionare colonne
      ↓
filtrare righe
```

Ora useremo quelle stesse operazioni per rispondere a una nuova domanda:

> Una volta selezionate le osservazioni, come possiamo descriverne il comportamento senza limitarci a guardare le righe una per una?

## In questa UD impariamo

- conteggio (`count`);
- minimo e massimo;
- media;
- mediana;
- perché è utile separare i gruppi;
- `groupby` come automazione di una separazione già compresa;
- percentile 95 (`p95`) come descrizione della parte lenta;
- grafico temporale semplice.

## Non stiamo ancora facendo

- baseline;
- MAD;
- soglie;
- anomaly detection;
- ground truth operativa;
- veri e falsi positivi;
- Machine Learning.

## Ordine consigliato

1. `00_OBS_UD27_Concetti_Statistica_Descrittiva_Gruppi_v7_0.md`
2. `02_OBS_UD27_ESEMPI_VISIVI_E_NUMERICI_v7_0.md`
3. `07_OBS_UD27_GUIDA_ARCHITETTURA_Dal_DataFrame_alla_Descrizione_v7_0.md`
4. `05_OBS_UD27_GUIDA_OPERATIVA_Pandas_Grafico_v7_0.md`
5. `01_OBS_UD27_LAB_guidato_Descrivere_Gruppi_v7_0.md`
6. `03_OBS_UD27_MINI_ATTIVITA_Statistiche_Gruppi_v7_0.md`
7. `04_OBS_UD27_LAB_autonomo_Confrontare_Due_Gruppi_v7_0.md`
8. `06_OBS_UD27_Raccordo_Verso_Baseline_v7_0.md`

## Competenza finale

> So descrivere e confrontare gruppi di osservazioni usando count, minimo, massimo, media, mediana e p95, senza confondere una statistica con una diagnosi.
