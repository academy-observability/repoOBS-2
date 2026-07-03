# UD09 - KQL per troubleshooting e aggregazioni

La UD09 riparte dalla UD08-02: il partecipante ha già creato o usato un Log Analytics Workspace, ha eseguito query KQL base e ha distinto query simulate da query su tabelle Azure reali.

L'obiettivo della UD09 è passare da query descrittive a query diagnostiche: contare errori, calcolare tassi, leggere trend temporali, identificare finestre anomale e preparare una query candidata per gli alert della UD10.

## Sequenza consigliata per i partecipanti

| Ordine | File | Quando usarlo | Scopo operativo |
|---:|---|---|---|
| 1 | `00_OBS_UD09_Concetti_KQL_Troubleshooting_Aggregazioni_v5_2.md` | Prima del laboratorio | Introduce metodo diagnostico, aggregazioni, error rate, percentili e trend temporali |
| 2 | `01_OBS_UD09_LAB_guidato_KQL_Troubleshooting_Aggregazioni_v5_2.md` | Laboratorio guidato | Esegue query su dataset `datatable()` e costruisce una prima diagnosi controllata |
| 3 | `04_OBS_UD09_GUIDA_OPERATIVA_KQL_Troubleshooting_Passo_Passo_v5_2.md` | Come supporto durante i laboratori | Spiega come eseguire query, salvare evidenze, leggere risultati vuoti o errori e usare la CLI in modo controllato |
| 4 | `05_OBS_UD09_LAB_guidato_Troubleshooting_Tabelle_Azure_Reali_v5_2.md` | Dopo il guidato o dopo la verifica UD08 dei Diagnostic settings | Applica lo stesso metodo a `AzureActivity`, `AppServiceHTTPLogs`, `StorageBlobLogs`, `AzureMetrics` e tabelle VM se presenti |
| 5 | `03_OBS_UD09_LAB_autonomo_Runbook_Investigazione_KQL_v5_2.md` | Sessione autonoma | Produce un runbook investigativo KQL riutilizzabile nella UD10 |
| 6 | `README.md` | Sempre come indice | Riepiloga file, cartelle operative e output atteso |

## Cartelle operative

| Cartella | Uso |
|---|---|
| `src/kql/local/` | query KQL didattiche basate su `datatable()` |
| `src/kql/azure/` | query KQL su tabelle reali del Log Analytics Workspace |
| `docs/` | template e report compilati |
| `evidence/` | screenshot, esportazioni e prove raccolte |
| `logs/` | output testuali locali |
| `config/` | configurazione di esempio per workspace e risorse |
| `img/` | immagini usate nei report |

## Output atteso

Al termine della UD09 il partecipante deve avere:

- report guidato compilato;
- almeno cinque query KQL eseguite su dataset simulato;
- almeno una verifica ragionata su tabelle Azure reali, anche se vuote o assenti;
- runbook investigativo autonomo;
- query candidata per un alert da usare nella UD10;
- evidenze salvate e commit finale.

## Regola operativa

Le query `datatable()` dimostrano il metodo KQL. Le query su tabelle reali dimostrano l'integrazione con Azure. Un risultato vuoto non è automaticamente un errore: può indicare assenza di dati, finestra temporale sbagliata, diagnostic setting mancante o ritardo di ingestione.
