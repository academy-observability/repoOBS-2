# UD09 - KQL troubleshooting e aggregazioni

La UD09 mantiene il dataset controllato per consolidare gli operatori KQL e aggiunge un percorso diagnostico su tabelle reali del workspace, con discovery iniziale e rami alternativi per AzureActivity, App Service, VM monitorate con AMA/DCR e AzureDiagnostics.

## Sequenza consigliata per i partecipanti

| Passo | File | Uso |
|---:|---|---|
| 1 | `00_OBS_UD09_Concetti.md` | Concetti dettagliati aggiornati |
| 2 | `01_OBS_UD09_LAB_guidato_KQL_Troubleshooting_Aggregazioni_v5_1.md` | Laboratorio guidato troubleshooting KQL |
| 3 | `03_OBS_UD09_LAB_autonomo_Runbook_Investigazione_KQL_v5_1.md` | Laboratorio autonomo runbook investigativo |
| 4 | `04_OBS_UD09_GUIDA_OPERATIVA_KQL_Passo_Passo_v5_1.md` | Guida operativa passo passo |
| 5 | `05_OBS_UD09_LAB_guidato_Troubleshooting_Tabelle_Azure_Reali_v5_1.md` | Estensione guidata su troubleshooting con tabelle Azure reali |

## Cartelle operative

| Cartella | Uso |
|---|---|
| `src/kql/` | query KQL didattiche e query su tabelle reali |
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
