# 06 - UD10 Laboratorio guidato integrativo: creazione reale di un Log Alert su LAW

## 1. Scopo del laboratorio

Questo file integra il laboratorio guidato UD10.

Nella UD09 abbiamo preparato query candidate per alert. In UD10 abbiamo analizzato soglie, Action Group, dashboard e workbook. In questo laboratorio integriamo il passaggio operativo mancante:

```text
query KQL su Log Analytics Workspace
→ condizione di alert
→ Action Group
→ Log Alert Rule reale
→ evidenze
```

L'obiettivo è creare almeno una **Log Alert Rule reale** su dati presenti nel Log Analytics Workspace.

## 2. Prerequisiti

Prima di iniziare verificare di avere:

- una Web App creata nelle UD precedenti;
- un Log Analytics Workspace già usato in UD08/UD09;
- Diagnostic settings della Web App collegati al LAW;
- tabella `AppServiceHTTPLogs` presente nel workspace;
- accesso al Portale Azure;
- cartella `UD10` aperta nel repository locale.

Se `AppServiceHTTPLogs` non restituisce dati recenti, usare il fallback su `AzureActivity` indicato in fondo al laboratorio.

## 3. Preparazione evidenze

Nel terminale, dalla cartella `UD10`, creare le cartelle di lavoro se non esistono:

```bash
mkdir -p evidence docs logs
```

Creare un file report dedicato:

```bash
cat > docs/report_ud10_06_log_alert_reale.md <<'REPORT'
# Report UD10 - Creazione reale Log Alert su LAW

## Ambiente

| Voce | Valore |
|---|---|
| Partecipante | |
| Data | |
| Log Analytics Workspace | |
| Web App | |
| Tabella usata | AppServiceHTTPLogs |

## Query di verifica tabella

- La tabella contiene dati recenti? Sì / No
- Ultimo record osservato:
- Evidenza salvata:

## Segnale generato

- URL chiamata:
- Codice HTTP ottenuto:
- Evidenza salvata:

## Query candidata per alert

- Query usata:
- Finestra temporale:
- Condizione:
- Soglia:
- Evidenza salvata:

## Action Group

- Nome Action Group:
- Tipo notifica:
- Destinatario:
- Evidenza salvata:

## Alert Rule

- Nome alert:
- Scope:
- Condizione:
- Frequenza valutazione:
- Periodo valutazione:
- Severità:
- Action Group associato:
- Evidenza salvata:

## Conclusione

Scrivere 5-8 righe spiegando perché l'alert è corretto per il laboratorio e quali limiti avrebbe in produzione.
REPORT
```

## 4. Task 1 - Verificare la tabella `AppServiceHTTPLogs`

Aprire il Portale Azure:

```text
Azure Portal
→ Log Analytics workspaces
→ workspace usato in UD08/UD09
→ Logs
```

Eseguire questa query:

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(24h)
| summarize
    Record=count(),
    Primo=min(TimeGenerated),
    Ultimo=max(TimeGenerated)
  by CsHost
| sort by Record desc
```

Output atteso:

```text
almeno una riga relativa alla Web App osservata
```

Salvare evidenza:

```text
evidence/ud10_06_01_appservicehttplogs_verifica.png
```

Se non ci sono dati recenti, proseguire con il Task 2 per generare traffico.

## 5. Task 2 - Generare un errore HTTP 4xx controllato

L'alert userà un errore 4xx controllato. Un 404 è adatto al laboratorio perché si genera facilmente visitando una URL inesistente della Web App.

Da browser o da terminale chiamare:

```bash
curl -i https://<nome-webapp>.azurewebsites.net/errore-ud10-test
```

Esempio:

```bash
curl -i https://app-obs-ud05-ep.azurewebsites.net/errore-ud10-test
```

Output atteso:

```text
HTTP 404 oppure altro codice 4xx
```

Salvare evidenza:

```text
evidence/ud10_06_02_errore_4xx_generato.png
```

Attendere alcuni minuti per l'ingestione nel Log Analytics Workspace.

## 6. Task 3 - Verificare il segnale nel LAW

Eseguire questa query:

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(30m)
| where ScStatus between (400 .. 499)
| project TimeGenerated, CsHost, CsUriStem, ScStatus, UserAgent
| sort by TimeGenerated desc
```

Output atteso:

```text
almeno una riga con codice HTTP 4xx
```

Idealmente deve comparire anche la chiamata verso:

```text
/errore-ud10-test
```

Salvare evidenza:

```text
evidence/ud10_06_03_query_4xx_dettaglio.png
```

## 7. Task 4 - Preparare la query finale da alert

Questa è la query che verrà usata nella Log Alert Rule:

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(30m)
| where ScStatus between (400 .. 499)
| summarize Errori4xx = count() by CsHost
| where Errori4xx > 0
```

Significato:

```text
se negli ultimi 30 minuti esiste almeno un errore HTTP 4xx sulla Web App, la query restituisce una riga
```

Per il laboratorio è una condizione utile perché consente di verificare tutta la catena:

```text
Web App
→ log HTTP
→ Log Analytics Workspace
→ query KQL
→ alert
→ Action Group
```

Nota importante:

```text
In produzione non sarebbe corretto generare un alert per un singolo 4xx.
In un ambiente reale si userebbe una soglia più robusta, per esempio molti 4xx in pochi minuti oppure un error rate percentuale.
```

Salvare evidenza:

```text
evidence/ud10_06_04_query_alert_candidata.png
```

## 8. Task 5 - Creare l'Action Group

Aprire:

```text
Azure Portal
→ Monitor
→ Alerts
→ Action groups
→ Create
```

Configurazione consigliata:

| Campo | Valore |
|---|---|
| Subscription | subscription del laboratorio |
| Resource group | resource group usato nel corso |
| Action group name | `ag-ud10-lab` |
| Display name | `UD10LAB` |
| Notification type | Email |
| Email | email del partecipante o email di laboratorio |

Salvare l'Action Group.

Evidenza richiesta:

```text
evidence/ud10_06_05_action_group.png
```

Nel report compilare:

```text
Nome Action Group: ag-ud10-lab
Tipo notifica: Email
Destinatario: <email usata>
```

## 9. Task 6 - Creare la Log Alert Rule

Aprire:

```text
Azure Portal
→ Monitor
→ Alerts
→ Create
→ Alert rule
```

### 9.1 Scope

Impostare come scope il Log Analytics Workspace usato in UD08/UD09/UD10.

```text
Scope: Log Analytics Workspace del corso
```

### 9.2 Condition

Selezionare:

```text
Custom log search
```

Inserire la query:

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(30m)
| where ScStatus between (400 .. 499)
| summarize Errori4xx = count() by CsHost
| where Errori4xx > 0
```

Configurazione della condizione:

| Campo | Valore |
|---|---|
| Measurement | Table rows |
| Aggregation granularity | 30 minutes |
| Operator | Greater than |
| Threshold value | 0 |
| Frequency of evaluation | 5 minutes |

Significato operativo:

```text
se la query restituisce almeno una riga, l'alert deve scattare
```

Evidenza richiesta:

```text
evidence/ud10_06_06_alert_condition.png
```

### 9.3 Actions

Associare l'Action Group creato nel Task 5:

```text
ag-ud10-lab
```

Evidenza richiesta:

```text
evidence/ud10_06_07_alert_action_group_associato.png
```

### 9.4 Details

Configurare:

| Campo | Valore |
|---|---|
| Severity | 3 |
| Alert rule name | `ud10-appservice-4xx-detected` |
| Description | `Alert didattico su errori HTTP 4xx rilevati nei log App Service` |
| Enable upon creation | Yes |

Evidenza richiesta:

```text
evidence/ud10_06_08_alert_details.png
```

### 9.5 Review + create

Verificare il riepilogo e creare l'alert.

Evidenza richiesta:

```text
evidence/ud10_06_09_alert_rule_created.png
```

## 10. Task 7 - Verifica finale

Dopo alcuni minuti verificare lo stato dell'alert:

```text
Azure Portal
→ Monitor
→ Alerts
→ Alert rules
→ ud10-appservice-4xx-detected
```

Se l'alert non risulta ancora attivo o non ha generato notifiche, non forzare conclusioni errate. Verificare:

| Controllo | Cosa verificare |
|---|---|
| Query | restituisce righe nel Logs editor? |
| Time range | la finestra di 30 minuti contiene il 4xx? |
| Frequenza | sono passati almeno 5 minuti? |
| Action Group | è associato correttamente? |
| Alert abilitato | la rule è enabled? |

Salvare evidenza:

```text
evidence/ud10_06_10_alert_rule_overview.png
```

## 11. Task 8 - Compilare il report

Completare:

```text
docs/report_ud10_06_log_alert_reale.md
```

Conclusione attesa, esempio:

```text
È stata creata una Log Alert Rule sul Log Analytics Workspace del corso.
La regola usa la tabella AppServiceHTTPLogs e intercetta errori HTTP 4xx negli ultimi 30 minuti.
La condizione configurata è "numero risultati > 0".
L'Action Group associato è ag-ud10-lab.
L'alert è didattico: in produzione non sarebbe sufficiente un singolo 4xx, ma servirebbe una soglia più robusta o un error rate.
```

## 12. Task 9 - Commit finale

Dal terminale:

```bash
git status
git add docs/report_ud10_06_log_alert_reale.md evidence/
git commit -m "UD10 create real LAW log alert"
git status
```

## 13. Fallback: alert su `AzureActivity`

Usare questa alternativa solo se `AppServiceHTTPLogs` non è utilizzabile.

### 13.1 Generare il segnale

Modificare un tag su una risorsa del Resource Group.

Esempio:

```text
Resource Group
→ scegliere una risorsa
→ Tags
→ aggiungere o modificare tag
```

Esempio tag:

```text
ud10-alert-test = true
```

### 13.2 Query di verifica

```kql
AzureActivity
| where TimeGenerated > ago(30m)
| where OperationNameValue has "WRITE"
| project TimeGenerated, OperationNameValue, ActivityStatusValue, ResourceGroup, Resource, Caller
| sort by TimeGenerated desc
```

### 13.3 Query alternativa da alert

```kql
AzureActivity
| where TimeGenerated > ago(30m)
| where OperationNameValue has "WRITE"
| summarize OperazioniWrite = count() by ResourceGroup, Caller
| where OperazioniWrite > 0
```

Configurazione alert:

| Campo | Valore |
|---|---|
| Scope | Log Analytics Workspace |
| Condition | Custom log search |
| Measurement | Table rows |
| Operator | Greater than |
| Threshold | 0 |
| Evaluation period | 30 minutes |
| Frequency | 5 minutes |
| Severity | 3 |
| Alert name | `ud10-azureactivity-write-detected` |

Nota:

```text
Questo fallback è meno applicativo rispetto ad AppServiceHTTPLogs, ma consente comunque di verificare la catena evento Azure → LAW → query KQL → alert.
```

## 14. Checklist conclusiva

Prima di chiudere il laboratorio verificare:

```text
[ ] query AppServiceHTTPLogs eseguita
[ ] errore 4xx generato
[ ] query finale da alert validata
[ ] Action Group creato
[ ] Log Alert Rule creata
[ ] alert abilitato
[ ] evidenze salvate
[ ] report compilato
[ ] commit finale eseguito
```
