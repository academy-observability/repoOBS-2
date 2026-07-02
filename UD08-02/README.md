# UD08 - Log Analytics Workspace e KQL base

La UD08 introduce Log Analytics Workspace e KQL. Il percorso mantiene i dataset `datatable()` come palestra controllata e aggiunge una parte su tabelle Azure reali generate da risorse create nelle UD precedenti.

## Sequenza consigliata per i partecipanti

| Ordine | File | Quando usarlo | Scopo operativo |
|---:|---|---|---|
| 1 | `00_OBS_UD08_Concetti_DETTAGLIATO_v5_3.md` | Concetti, lessico e distinzione tra query simulata e query reale |
| 2 | `01_OBS_UD08_LAB_guidato_Log_Analytics_KQL_Base_v5_3.md` | Laboratorio guidato KQL base su workspace e `datatable()` |
| 3 | `04_OBS_UD08_GUIDA_OPERATIVA_KQL_Passo_Passo_v5_3.md` | Come supporto durante i laboratori | Spiega come eseguire manualmente query da file `.kql`, salvare JSON, leggere errori e produrre evidenze senza script automatici |
| 4 | `06_OBS_UD08_GUIDA_PORTALE_Collegamenti_Risorse_LAW_v5_4.md` | Prima o insieme al laboratorio 05 | Mostra da Portale Azure come collegare Activity Log, Storage Blob, Web App e VM al LAW |
| 5 | `05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_4_partecipanti.md` | Dopo il percorso KQL base | Esegue la parte tecnica completa: individua le risorse UD05 del partecipante, crea diagnostic settings, genera traffico, interroga tabelle reali |
| 6 | `03_OBS_UD08_LAB_autonomo_Query_Card_KQL_v5_3.md` | Dopo il guidato, preferibilmente dopo il laboratorio 05 | Produce la Query Card autonoma. A questo punto il partecipante può confrontare query simulate e almeno una tabella reale, se disponibile |
| 7 | `README.md` | Sempre come indice | Riepiloga file, cartelle operative e output atteso della UD08 |




## Cartelle operative

| Cartella | Uso |
|---|---|
| `src/kql/local/` | query KQL didattiche basate su `datatable()` |
| `src/kql/azure/` | query KQL su tabelle reali del Log Analytics Workspace |
| `docs/` | template di report e documentazione prodotta |
| `evidence/` | screenshot, esportazioni e prove raccolte |
| `logs/` | output testuali locali |
| `config/` | file di configurazione di esempio |
| `img/` | immagini usate nei report |

## Regola operativa su Azure Portal, terminale locale e Cloud Shell

Le query KQL si eseguono nel Logs editor del portale Azure oppure, dove indicato, con Azure CLI da terminale locale autenticato. I comandi che salvano file in `docs/`, `evidence/`, `logs/` o `img/` vanno eseguiti nel repository locale o in WSL. Cloud Shell è utile per controlli rapidi sul tenant Azure, ma non coincide con la repository locale.

## Output atteso

Al termine della UD il partecipante deve avere query KQL eseguite, evidenze salvate, report compilati e una distinzione chiara tra dataset didattici `datatable()` e tabelle Azure reali.
