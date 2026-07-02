# UD08 - Log Analytics Workspace e KQL base

La UD08 mantiene i dataset `datatable()` come palestra KQL e aggiunge un percorso esplicito su tabelle reali del workspace: `AzureActivity`, `AzureMetrics`, log App Service, tabelle VM via AMA/DCR e `AzureDiagnostics` quando disponibili.

## Sequenza consigliata per i partecipanti

| Passo | File | Uso |
|---:|---|---|
| 1 | `00_OBS_UD08_Concetti_DETTAGLIATO_v5_2.md` | Concetti dettagliati aggiornati |
| 2 | `01_OBS_UD08_LAB_guidato_Log_Analytics_KQL_Base_v5_2.md` | Laboratorio guidato KQL base |
| 3 | `03_OBS_UD08_LAB_autonomo_Query_Card_KQL_v5_2.md` | Laboratorio autonomo Query Card |
| 4 | `04_OBS_UD08_GUIDA_OPERATIVA_KQL_Passo_Passo_v5_2.md` | Guida operativa passo passo |
| 5 | `05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_2.md` | Estensione guidata su tabelle Azure reali |

## Cartelle operative

| Cartella | Uso |
|---|---|
| `src/kql/local/` | query KQL didattiche basate su `datatable()` |
| `src/kql/azure/` | query KQL su tabelle reali del workspace |
| `docs/` | template di report e documentazione prodotta |
| `evidence/` | screenshot, esportazioni e prove raccolte |
| `logs/` | eventuali output testuali locali |
| `config/` | file di configurazione di esempio |
| `img/` | immagini usate nei report |

## Regola operativa su Azure Portal, terminale locale e Cloud Shell

Le query KQL si eseguono nel Logs editor del portale Azure oppure, dove indicato, con strumenti locali già autenticati. Le evidenze da salvare nella repository vanno create nel terminale locale o WSL. Cloud Shell è utile per controlli rapidi sul tenant Azure, ma non coincide con la repository locale dei partecipanti.

## Output atteso

Al termine della UD il partecipante deve avere:

- query KQL eseguite e comprese;
- evidenze salvate in `evidence/`;
- report compilato in `docs/`;
- distinzione chiara tra dataset didattici `datatable()` e tabelle Azure reali.
