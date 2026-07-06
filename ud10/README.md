# UD10 - Alert, Action Group, Dashboard e Workbook

## Scopo della UD

La UD10 conclude il primo blocco operativo su Azure Monitor e Log Analytics. Dopo UD08 e UD09 sappiamo creare query KQL e usarle per un'indagine. In questa unità decidiamo quali query possono diventare alert, quali sono più adatte a dashboard/workbook e come documentare un piccolo monitoring pack.

```text
UD08 -> Log Analytics Workspace e KQL base
UD09 -> KQL per troubleshooting e aggregazioni
UD10 -> alert, action group, dashboard, workbook e monitoring pack
```

## Sequenza consigliata

| Passo | File | Uso |
|---:|---|---|
| 1 | `00_OBS_UD10_Concetti_Alert_Dashboard_Workbook_v5_2.md` | Concetti: alert, soglie, severità, action group, dashboard, workbook |
| 2 | `01_OBS_UD10_LAB_guidato_Alert_Action_Group_Dashboard_Workbook_v5_2.md` | Laboratorio guidato con query simulate e progettazione alert |
| 3 | `04_OBS_UD10_GUIDA_OPERATIVA_Alert_Workbook_Passo_Passo_v5_2.md` | Guida rapida per eseguire i passaggi senza perdersi nel portale |
| 4 | `05_OBS_UD10_LAB_guidato_Workbook_Alert_Tabelle_Azure_Reali_v5_2.md` | Estensione su dati reali del Log Analytics Workspace, se disponibili |
| 5 | `03_OBS_UD10_LAB_autonomo_Monitoring_Pack_Azure_v5_2.md` | Attività autonoma: costruzione del monitoring pack |

## Cartelle operative

| Cartella | Contenuto |
|---|---|
| `src/kql/alert/` | query candidate per alert su dataset didattici |
| `src/kql/workbook/` | query per dashboard e workbook su dataset didattici |
| `src/kql/azure/` | query adattabili alle tabelle reali del workspace |
| `docs/` | template da compilare |
| `evidence/` | screenshot, esportazioni e output di verifica |
| `logs/` | eventuali output testuali |
| `config/` | variabili e note operative |
| `img/` | immagini da includere nei report |

## Output atteso

Alla fine della UD10 devono essere presenti almeno:

- una query candidata per alert con soglia motivata;
- un Alert Decision Record compilato;
- una bozza di dashboard o workbook;
- un monitoring pack minimo in `docs/`;
- evidenze salvate in `evidence/`;
- nota sui limiti dei dati reali disponibili nel workspace.

## Regola pratica

Una query che restituisce righe non è automaticamente un buon alert. Una query diventa candidata per alert solo quando produce una condizione azionabile, con soglia, finestra temporale, severità e azione successiva chiare.
