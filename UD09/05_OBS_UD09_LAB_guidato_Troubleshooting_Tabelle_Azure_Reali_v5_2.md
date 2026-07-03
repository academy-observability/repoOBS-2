# 05 - UD09 Laboratorio guidato: troubleshooting su tabelle Azure reali

## 1. Obiettivo

Applicare il metodo della UD09 alle tabelle reali configurate durante UD08.

Il risultato atteso non è “tutte le tabelle piene”. Il risultato atteso è saper distinguere:

```text
tabella presente con dati
tabella presente ma vuota
tabella assente
query sbagliata
finestra temporale sbagliata
```

## 2. Prerequisiti

Avere completato almeno la parte UD08 relativa a:

- Log Analytics Workspace;
- collegamento Activity Log verso LAW;
- Diagnostic settings per Storage Blob o Web App, se disponibili;
- eventuale VM con Azure Monitor Agent e Data Collection Rule.

## 3. Preparare il report

```bash
cp docs/template_report_ud09_troubleshooting_azure_reale.md docs/report_ud09_troubleshooting_azure_reale.md
mkdir -p evidence logs
```

## 4. Scoprire quali tabelle sono disponibili

Nel Logs editor eseguire:

```text
src/kql/azure/01_scopri_tabelle_note_workspace.kql
```

Annotare nel report:

```text
tabelle trovate
numero record ultime 24 ore
prima e ultima occorrenza
```

Evidenza:

```text
evidence/ud09_azure_01_tabelle_note.png
```

## 5. AzureActivity

Se `AzureActivity` è disponibile, eseguire:

```text
src/kql/azure/02_azureactivity_operazioni_fallite.kql
src/kql/azure/03_azureactivity_trend_orario.kql
```

Interpretare:

```text
ci sono operazioni fallite?
quale Resource Group è più coinvolto?
il trend mostra una finestra concentrata?
```

## 6. App Service HTTP Logs

Se `AppServiceHTTPLogs` è disponibile, eseguire:

```text
src/kql/azure/04_appservice_errori_http.kql
```

Se è vuota:

```text
verificare Diagnostic settings della Web App
generare traffico HTTP verso la Web App
attendere ingestione
riallargare il time range
```

## 7. Storage Blob Logs

Se `StorageBlobLogs` è disponibile, eseguire:

```text
src/kql/azure/05_storageblob_operazioni_errori.kql
```

Se è vuota, caricare o leggere un blob dopo avere configurato il diagnostic setting.

## 8. AzureMetrics

Se `AzureMetrics` è disponibile, eseguire:

```text
src/kql/azure/06_azuremetrics_risorse_trend.kql
```

Verificare quali risorse e metriche sono presenti.

## 9. VM: Heartbeat e Perf

Se la VM è stata collegata con AMA/DCR, eseguire:

```text
src/kql/azure/07_vm_heartbeat_perf.kql
```

Interpretare:

```text
la VM invia heartbeat?
l'ultimo heartbeat è recente?
sono disponibili metriche Perf?
```

## 10. Fallback AzureDiagnostics

Solo se l'ambiente usa ancora tabelle legacy:

```text
src/kql/azure/08_azurediagnostics_errori_fallback.kql
```

Non trattare `AzureDiagnostics` come percorso standard se le tabelle resource-specific sono disponibili.

## 11. Conclusione del report

Scrivere una conclusione sintetica:

```text
Le tabelle reali disponibili sono ...
La tabella più utile per il troubleshooting attuale è ...
Il limite principale dell'ambiente è ...
La query candidata per UD10 è ...
```

## 12. Commit finale

```bash
git status
git add docs/report_ud09_troubleshooting_azure_reale.md evidence/ logs/
git commit -m "UD09 real Azure tables troubleshooting"
```
