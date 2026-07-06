# 07 - UD10 Completamento: Dashboard e Workbook reali nel Portale Azure

## 1. Scopo

Questo file serve a completare la parte della UD10 su Dashboard e Workbook, evitando ambiguità tra:

```text
bozza progettuale
```

e

```text
visualizzazione reale nel Portale Azure
```

L'obiettivo minimo è mostrare almeno una query KQL in una vista operativa: Dashboard oppure Workbook.

## 2. Differenza pratica

| Oggetto | A cosa serve | Quando usarlo |
|---|---|---|
| Dashboard | vista rapida e sintetica | controllo immediato di pochi indicatori |
| Workbook | percorso di analisi con testo, query, parametri e visualizzazioni | diagnosi guidata e report operativo |

Per UD10 è accettabile completare almeno uno dei due. Il Workbook è preferibile se si vuole spiegare il ragionamento diagnostico.

---

# Parte A - Creare o visualizzare una Dashboard

## 3. Query consigliata per Dashboard

Aprire:

```text
Azure Portal -> Log Analytics workspaces -> workspace UD08/UD09 -> Logs
```

Eseguire una query semplice e visualizzabile. Esempio su App Service:

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(1h)
| summarize Richieste=count() by bin(TimeGenerated, 5m)
| sort by TimeGenerated asc
```

Se `AppServiceHTTPLogs` non ha dati recenti, usare una query su `AzureActivity`:

```kql
AzureActivity
| where TimeGenerated > ago(24h)
| summarize Operazioni=count() by bin(TimeGenerated, 1h)
| sort by TimeGenerated asc
```

## 4. Visualizzazione

Nel risultato della query scegliere una visualizzazione coerente:

```text
Chart / Time chart
```

oppure, se disponibile:

```text
Visualization -> Time chart
```

## 5. Pin su Dashboard

Se il Portale mostra il comando:

```text
Pin to dashboard
```

procedere così:

```text
Pin to dashboard
-> Create new oppure scegliere dashboard esistente
-> nome dashboard: dash-ud10-monitoring
-> confermare
```

Poi aprire:

```text
Azure Portal -> Dashboard
```

Verificare che il pannello sia visibile.

## 6. Evidenze Dashboard

Salvare almeno:

```text
evidence/ud10_07_query_dashboard.png
evidence/ud10_07_dashboard_portale.png
```

Nel report annotare:

```text
Nome dashboard:
Query usata:
Indicatore mostrato:
Perché è utile:
Limite della vista:
```

---

# Parte B - Creare un Workbook reale

## 7. Aprire Workbooks

Percorso:

```text
Azure Portal
-> Monitor
-> Workbooks
-> New
```

In alcune interfacce Azure il percorso può essere:

```text
Log Analytics Workspace
-> Workbooks
-> New
```

## 8. Struttura minima del Workbook

Creare un Workbook con tre blocchi:

```text
1. Titolo e scenario
2. Query di sintesi
3. Query di dettaglio o trend
```

## 9. Blocco 1 - Testo introduttivo

Aggiungere un blocco **Text** con un testo simile:

```text
# UD10 - Workbook operativo

Scenario: osservazione di una Web App o di una risorsa Azure collegata al Log Analytics Workspace.

Obiettivo: visualizzare segnali utili per supportare una decisione di alert e una prima diagnosi.
```

## 10. Blocco 2 - Query di sintesi

Aggiungere un blocco **Query**.

Data source:

```text
Logs
```

Resource:

```text
Log Analytics Workspace usato in UD08/UD09/UD10
```

Query consigliata su App Service:

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(1h)
| summarize
    Richieste=count(),
    Errori4xx=countif(ScStatus between (400 .. 499)),
    Errori5xx=countif(ScStatus between (500 .. 599))
  by CsHost
| extend ErrorRate4xx = iff(Richieste == 0, 0.0, round(100.0 * Errori4xx / Richieste, 2))
| sort by Richieste desc
```

Visualizzazione consigliata:

```text
Grid / Table
```

## 11. Blocco 3 - Query di trend

Aggiungere un secondo blocco **Query**.

```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(1h)
| summarize
    Richieste=count(),
    Errori4xx=countif(ScStatus between (400 .. 499))
  by bin(TimeGenerated, 5m)
| sort by TimeGenerated asc
```

Visualizzazione consigliata:

```text
Time chart
```

## 12. Se AppServiceHTTPLogs non è utilizzabile

Usare `AzureActivity`:

```kql
AzureActivity
| where TimeGenerated > ago(24h)
| summarize Operazioni=count() by OperationNameValue
| sort by Operazioni desc
```

E per il trend:

```kql
AzureActivity
| where TimeGenerated > ago(24h)
| summarize Operazioni=count() by bin(TimeGenerated, 1h)
| sort by TimeGenerated asc
```

## 13. Salvataggio Workbook

Salvare il Workbook con nome:

```text
wb-ud10-monitoring
```

Se non si dispone dei permessi per salvare, è accettabile salvare screenshot del Workbook non salvato.

## 14. Evidenze Workbook

Salvare:

```text
evidence/ud10_07_workbook_testo.png
evidence/ud10_07_workbook_query_sintesi.png
evidence/ud10_07_workbook_trend.png
```

## 15. Conclusione richiesta

Compilare nel report:

```text
Oggetto creato: Dashboard / Workbook
Query principale:
Indicatore mostrato:
Uso operativo:
Limite:
Collegamento con alert:
```

Esempio di conclusione:

```text
Il Workbook mostra richieste ed errori HTTP della Web App. La query di sintesi aiuta a capire se il servizio sta generando errori 4xx/5xx. La query di trend permette di osservare quando gli errori si concentrano. Il Workbook non sostituisce l'alert, ma aiuta a interpretare la condizione che l'alert segnala.
```
