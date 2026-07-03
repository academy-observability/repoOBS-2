# 03 - UD09 Laboratorio autonomo: runbook di investigazione KQL

## 1. Obiettivo

Produrre un runbook investigativo KQL. Il runbook deve spiegare quale sequenza di query useremmo davanti a un sospetto problema applicativo o infrastrutturale.

Non basta incollare query. Serve collegare ogni query a una domanda diagnostica.

## 2. Scenario

Il team riceve questa segnalazione:

```text
Durante una finestra recente alcuni utenti hanno segnalato lentezza e operazioni fallite.
Non è chiaro se il problema riguarda tutte le componenti o solo una parte del servizio.
```

## 3. Vincoli

Il lavoro deve usare:

- almeno quattro query da `src/kql/local/`;
- almeno una query da `src/kql/azure/`, se una tabella reale è disponibile;
- il template `docs/template_report_ud09_autonomo.md`;
- evidenze salvate in `evidence/`.

Se non ci sono tabelle reali disponibili, indicare chiaramente quale query Azure è stata provata e perché non ha prodotto dati.

## 4. Preparazione

```bash
cp docs/template_report_ud09_autonomo.md docs/report_ud09_autonomo.md
mkdir -p evidence logs
```

## 5. Task autonomi

### Task 1 - Definire le domande diagnostiche

Nel report scrivere almeno quattro domande. Esempio:

```text
Quale risorsa ha il tasso di errore più alto?
In quale finestra temporale si concentrano gli errori?
Quale operazione ha P95 più elevato?
La query può diventare un alert?
```

### Task 2 - Eseguire query su dataset simulato

Eseguire almeno quattro query tra:

```text
src/kql/local/02_error_rate_per_risorsa.kql
src/kql/local/03_trend_temporale_errori_bin_15m.kql
src/kql/local/04_latenza_percentili_p95_p99.kql
src/kql/local/05_top_operazioni_lente.kql
src/kql/local/06_finestra_incidente_candidata.kql
src/kql/local/07_query_alert_candidata.kql
```

Per ogni query indicare:

```text
domanda diagnostica
risultato osservato
interpretazione
limite della query
```

### Task 3 - Verificare almeno una tabella Azure reale

Eseguire prima:

```text
src/kql/azure/01_scopri_tabelle_note_workspace.kql
```

Poi scegliere una query coerente con le tabelle disponibili:

```text
AzureActivity -> 02 o 03
AppServiceHTTPLogs -> 04
StorageBlobLogs -> 05
AzureMetrics -> 06
Heartbeat/Perf -> 07
AzureDiagnostics -> 08
```

Se la tabella è assente o vuota, non inventare dati. Documentare il risultato.

### Task 4 - Scrivere una diagnosi sintetica

La diagnosi deve essere asciutta:

```text
Il problema principale emerge su ...
La finestra più critica è ...
Gli indicatori che supportano l'ipotesi sono ...
La causa non è dimostrata completamente perché ...
```

### Task 5 - Preparare la query candidata per UD10

Scegliere una query da trasformare in alert nella UD10. Indicare:

```text
nome query
soglia
finestra temporale
perché sarebbe utile come alert
rischio di falso positivo/falso negativo
```

## 6. Commit finale

```bash
git status
git add docs/report_ud09_autonomo.md evidence/ logs/
git commit -m "UD09 autonomous KQL investigation runbook"
```
