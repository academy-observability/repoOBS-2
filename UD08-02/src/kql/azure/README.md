# Query KQL su tabelle Azure reali

Queste query interrogano tabelle realmente presenti, se popolate, nel Log Analytics Workspace.

Le tabelle possono variare tra partecipanti perché dipendono dalle risorse create, dalla configurazione di raccolta, dal tempo di ingestione e dal percorso di monitoraggio usato dal servizio.

File principali:

| File | Uso |
|---|---|
| `01_scopri_tabelle_note_workspace.kql` | discovery delle tabelle note popolate |
| `02_usage_summary.kql` | riepilogo dei tipi di dato presenti nel workspace |
| `03_azureactivity_attivita_recenti.kql` | prime attività amministrative Azure |
| `04_azureactivity_operazioni_per_stato.kql` | aggregazione per stato attività |
| `05_azuremetrics_metriche_disponibili.kql` | metriche esportate nel workspace, se presenti |
| `06_appservice_http_status.kql` | riepilogo stato HTTP App Service |
| `07_vm_ama_dcr_tabelle_disponibili.kql` | verifica tabelle VM con AMA/DCR |
| `10_azureactivity_ud05_recent.kql` | attività recenti collegate alle risorse UD05 |
| `11_storagebloblogs_ud05_recent.kql` | operazioni recenti sul Blob service |
| `12_appservicehttplogs_ud05_recent.kql` | richieste HTTP recenti App Service |
| `13_realtables_summary_ud08.kql` | riepilogo finale delle tabelle reali |

Per le VM il percorso moderno è basato su Azure Monitor Agent, Data Collection Rules, VM Insights o Enhanced monitoring. La vecchia diagnostica VM basata su Azure Diagnostics Extension non è il percorso standard del laboratorio.
