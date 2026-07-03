# 01 - UD09 Laboratorio guidato: KQL troubleshooting e aggregazioni

## 1. Obiettivo

Costruire una diagnosi KQL controllata partendo da un dataset simulato. Alla fine del laboratorio dobbiamo saper rispondere a questa domanda:

```text
Quale componente mostra il problema più evidente e in quale finestra temporale?
```

## 2. Prerequisiti

Sono richiesti:

- repository locale aggiornato fino a UD08-02;
- accesso al Log Analytics Workspace usato in UD08;
- Azure Portal funzionante;
- terminale locale o WSL aperto nella cartella `UD09`.

Le query principali usano `datatable()`, quindi funzionano anche se il workspace non contiene ancora tabelle reali.

## 3. Preparazione cartelle e report

Aprire il terminale nella cartella `UD09`.

```bash
pwd
mkdir -p docs evidence logs
cp docs/template_report_ud09_guidato.md docs/report_ud09_guidato.md
ls -l docs/report_ud09_guidato.md
```

Annotare nel report:

```text
nome workspace usato
modalità di esecuzione: Portal Logs editor oppure CLI
cartella locale del repository
```

## 4. Aprire Logs nel Portale Azure

Percorso:

```text
Azure Portal
-> Log Analytics workspaces
-> workspace usato in UD08
-> Logs
```

Salvare uno screenshot dell'editor in:

```text
evidence/ud09_logs_editor.png
```

## 5. Query 01: dataset delle operazioni

Aprire il file:

```text
src/kql/local/01_dataset_operazioni.kql
```

Copiare la query nel Logs editor ed eseguirla.

Nel report indicare:

- quante righe restituisce;
- quali colonne sono più utili per la diagnosi;
- quali risorse compaiono nel dataset.

Evidenza:

```text
evidence/ud09_01_dataset.png
```

## 6. Query 02: error rate per risorsa

Eseguire:

```text
src/kql/local/02_error_rate_per_risorsa.kql
```

Rispondere nel report:

```text
Quale risorsa ha il tasso di errore più alto?
Il numero assoluto di errori coincide con il tasso più grave?
La latenza massima conferma o indebolisce l'ipotesi?
```

Evidenza:

```text
evidence/ud09_02_error_rate.png
```

## 7. Query 03: trend temporale degli errori

Eseguire:

```text
src/kql/local/03_trend_temporale_errori_bin_15m.kql
```

Questa query usa `bin(TimeGenerated, 15m)`. Individuare la finestra con più errori o error rate più alto.

Nel report indicare:

```text
finestra temporale più critica
numero eventi
numero errori
error rate
```

## 8. Query 04: latenza e percentili

Eseguire:

```text
src/kql/local/04_latenza_percentili_p95_p99.kql
```

Rispondere:

```text
Quale operation ha il P95 più alto?
La media da sola sarebbe sufficiente?
Cosa mostra il confronto tra media, massimo e P95?
```

## 9. Query 05: top operazioni lente

Eseguire:

```text
src/kql/local/05_top_operazioni_lente.kql
```

Usare i record più lenti per verificare se il problema riguarda sempre la stessa operazione o più componenti.

## 10. Query 06: finestra incidente candidata

Eseguire:

```text
src/kql/local/06_finestra_incidente_candidata.kql
```

Nel report scrivere una mini-diagnosi:

```text
La finestra candidata di incidente è ...
Il componente più coinvolto sembra ...
Gli indicatori principali sono ...
```

## 11. Query 07: query candidata per alert

Eseguire:

```text
src/kql/local/07_query_alert_candidata.kql
```

Questa query è preparatoria alla UD10. Non stiamo ancora creando l'alert, ma stiamo verificando se la condizione diagnostica è esprimibile con KQL.

Nel report annotare:

```text
soglia usata
condizione osservata
perché la query può diventare alert
limite della query
```

## 12. Salvataggio evidenze da CLI, opzionale

Se si vuole salvare l'output JSON di una query, usare `az monitor log-analytics query` dopo avere valorizzato `WORKSPACE_ID`.

```bash
source config/ud09.env

az monitor log-analytics query   --workspace "$WORKSPACE_ID"   --analytics-query "$(cat src/kql/local/02_error_rate_per_risorsa.kql)"   --output json > evidence/ud09_02_error_rate.json
```

Se il comando fallisce, completare il laboratorio dal Portale e documentare l'errore nel report.

## 13. Commit finale

```bash
git status
git add docs/report_ud09_guidato.md evidence/ logs/ src/kql/
git commit -m "UD09 guided KQL troubleshooting"
git status
```

Se non ci sono nuove evidenze binarie da aggiungere, il commit può includere solo il report compilato.
