# 03 - UD10 Laboratorio autonomo

## Monitoring Pack Azure

## 1. Obiettivo

Costruire un monitoring pack minimo partendo da uno scenario operativo. Il lavoro autonomo non deve ripetere il laboratorio guidato: deve prendere una decisione motivata.

Output principale:

```text
docs/monitoring_pack_ud10_autonomo.md
```

## 2. Scenario

Scegliere uno scenario tra quelli proposti.

| Scenario | Descrizione | Focus |
|---|---|---|
| A | Errori applicativi HTTP | error rate, 5xx, trend |
| B | Operazioni Azure fallite | AzureActivity, attività amministrative |
| C | Storage con errori operativi | StorageBlobLogs o AzureDiagnostics |
| D | VM non più osservabile | Heartbeat / Perf, se disponibili |
| E | Scenario simulato completo | dataset `datatable()` quando i dati reali mancano |

La scelta deve essere compatibile con i dati disponibili. Se una tabella reale è assente, documentare l'assenza e usare lo scenario simulato.

## 3. Attività richieste

Compilare:

```bash
cp docs/template_monitoring_pack_ud10.md docs/monitoring_pack_ud10_autonomo.md
cp docs/template_alert_decision_record_ud10.md docs/alert_decision_record_autonomo.md
cp docs/template_workbook_outline_ud10.md docs/workbook_outline_autonomo.md
```

Nel monitoring pack devono essere presenti:

1. scenario scelto;
2. sorgente dati usata;
3. query principale;
4. query candidate per dashboard/workbook;
5. query candidata per alert;
6. soglia motivata;
7. finestra e frequenza di valutazione;
8. severità;
9. Action Group progettato;
10. prima azione di verifica;
11. rischio di falso positivo;
12. limiti dei dati disponibili.

## 4. Vincoli tecnici

Usare almeno:

- una query candidata per alert;
- una query per trend temporale;
- una query di dettaglio;
- un output testuale o screenshot per evidenza.

Le query possono essere:

```text
src/kql/alert/*
src/kql/workbook/*
src/kql/azure/*
```

Le query reali Azure vanno usate solo se la tabella esiste e contiene dati recenti.

## 5. Criteri di qualità

| Criterio | Cosa viene valutato |
|---|---|
| Coerenza | scenario, query, soglia e azione sono collegati |
| Azionabilità | l'alert indica cosa fare dopo |
| Rumore | la soglia non produce notifiche inutili |
| Visualizzazione | dashboard/workbook rispondono a domande chiare |
| Evidenze | screenshot/output sono salvati e commentati |
| Limiti | il report dichiara cosa non è disponibile |

## 6. Domande guida

Rispondere nel report:

```text
Quale rischio operativo vuoi rilevare?
Quale segnale lo rappresenta?
La query restituisce una condizione o solo un elenco di eventi?
La soglia è motivata o casuale?
La finestra temporale è coerente con il fenomeno?
Che cosa deve fare chi riceve l'alert?
Quale pannello aiuta a capire se l'alert è reale?
Quale limite dei dati può rendere debole la decisione?
```

## 7. Evidenze da produrre

Salvare in `evidence/`:

```text
ud10_autonomo_query_alert.png
ud10_autonomo_query_workbook.png
ud10_autonomo_discovery_tabelle.png, se si usano dati reali
ud10_autonomo_git_status.txt
```

Comando finale:

```bash
find docs evidence -maxdepth 2 -type f | sort | tee evidence/ud10_autonomo_file_list.txt
git status --short | tee evidence/ud10_autonomo_git_status.txt
```

## 8. Consegna

La consegna è valida se nel repository sono presenti:

```text
docs/monitoring_pack_ud10_autonomo.md
docs/alert_decision_record_autonomo.md
docs/workbook_outline_autonomo.md
evidence/ud10_autonomo_file_list.txt
evidence/ud10_autonomo_git_status.txt
```

La qualità della consegna non dipende dal numero di pannelli creati, ma dalla solidità della decisione tecnica.
