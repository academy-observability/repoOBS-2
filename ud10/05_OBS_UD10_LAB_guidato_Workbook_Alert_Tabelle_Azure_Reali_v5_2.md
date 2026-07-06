# 05 - UD10 Laboratorio guidato aggiuntivo

## Workbook e alert con tabelle Azure reali

## 1. Obiettivo

Questo laboratorio collega UD10 ai dati reali del Log Analytics Workspace creato in UD08 e usato in UD09.

L'obiettivo non è forzare un risultato. L'obiettivo è capire quali dati reali esistono e costruire solo workbook/alert coerenti con le sorgenti disponibili.

## 2. Punto di partenza

Eseguire sempre prima la discovery:

```text
src/kql/azure/01_discovery_tabelle_workspace_ud10.kql
```

Questa query verifica la presenza di tabelle note e il numero di righe recenti.

## 3. Caso AzureActivity

Se `AzureActivity` contiene dati recenti, usare:

```text
src/kql/azure/02_workbook_azureactivity_stati.kql
src/kql/azure/03_workbook_azureactivity_timechart.kql
src/kql/azure/04_alert_azureactivity_errori_recenti.kql
```

Uso consigliato:

| Query | Oggetto |
|---|---|
| stati | tile o tabella workbook |
| timechart | grafico temporale |
| errori recenti | candidata alert |

Domanda operativa:

```text
Ci sono operazioni amministrative fallite in modo recente o ricorrente?
```

## 4. Caso App Service

Se `AppServiceHTTPLogs` contiene dati recenti, usare:

```text
src/kql/azure/05_workbook_appservice_http_status.kql
src/kql/azure/06_alert_appservice_5xx_recenti.kql
```

Domande operative:

```text
Gli errori HTTP sono concentrati in una finestra temporale?
Ci sono errori 5xx recenti oltre una soglia ragionevole?
```

Una soglia minima didattica può essere:

```text
errori_5xx >= 3 negli ultimi 15 minuti
```

Va comunque motivata in base al traffico reale.

## 5. Caso Storage Account

Se `StorageBlobLogs` contiene dati recenti, usare:

```text
src/kql/azure/07_workbook_storageblob_status.kql
src/kql/azure/08_alert_storageblob_errori_recenti.kql
```

Domanda operativa:

```text
Le operazioni sul Blob Storage producono errori ricorrenti?
```

Se la tabella è assente, controllare che i Diagnostic settings dello Storage Account siano stati configurati verso il workspace e che sia trascorso tempo sufficiente.

## 6. Caso VM con Azure Monitor Agent

Se `Heartbeat` contiene dati recenti, usare:

```text
src/kql/azure/09_workbook_vm_heartbeat.kql
src/kql/azure/10_alert_vm_heartbeat_assente.kql
```

Domanda operativa:

```text
La VM sta ancora inviando heartbeat al workspace?
```

Per le VM il percorso standard del corso è Azure Monitor Agent con Data Collection Rules o VM Insights. Non usare la diagnostica VM legacy come percorso principale.

## 7. Fallback AzureDiagnostics

Se le tabelle specifiche non sono presenti ma `AzureDiagnostics` contiene dati, usare:

```text
src/kql/azure/11_fallback_azurediagnostics_errori.kql
```

Questa query è un fallback. Nel report va scritto che lo schema di `AzureDiagnostics` può variare in base al servizio.

## 8. Compilazione report reale

Creare il report:

```bash
cp docs/template_monitoring_pack_azure_reale_ud10.md docs/monitoring_pack_azure_reale_ud10.md
```

Compilare almeno:

```text
Tabelle trovate
Tabelle assenti
Query usate
Oggetto costruito: dashboard, workbook o alert
Soglia proposta
Limiti dei dati disponibili
Evidenze
```

## 9. Criterio di qualità

Non costruire alert su tabelle assenti o vuote.

Una consegna corretta può dire:

```text
La tabella AppServiceHTTPLogs non è disponibile nel workspace. Per questo scenario non creo alert HTTP reale. Uso una query didattica per la forma e documento il prerequisito mancante.
```

Questa risposta è tecnicamente migliore di una configurazione fittizia.

## 10. Evidenze finali

Salvare in `evidence/`:

```text
ud10_discovery_tabelle_reali.png
ud10_query_reale_workbook.png, se disponibile
ud10_query_reale_alert.png, se disponibile
ud10_limiti_dati_reali.txt, se alcune tabelle mancano
```

Comando utile:

```bash
find docs evidence -maxdepth 2 -type f | sort | tee evidence/ud10_azure_reale_file_list.txt
```
