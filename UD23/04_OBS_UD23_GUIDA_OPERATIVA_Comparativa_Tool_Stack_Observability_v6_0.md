# OBS UD23 - Guida operativa
# Comparativa tool e stack Observability

## 0. Scopo della guida

Questa guida aiuta a raccogliere evidenze senza disperdersi tra strumenti. La UD23 non chiede di diventare esperti di tutti i tool; chiede di confrontare viste diverse sulla stessa applicazione e arrivare a una scelta motivata.

## 1. Evidenze Prometheus

Percorso:

```text
http://localhost:9090
```

Query utili:

```promql
up
```

```promql
sum(rate(http_requests_total[5m])) by (service, path)
```

```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, path)
```

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service, path))
```

Cosa annotare:

| Evidenza | Nota |
|---|---|
| target UP/DOWN | availability tecnica |
| request rate | volume traffico |
| error rate | endpoint problematico |
| p95 latency | lentezza percepibile |

## 2. Evidenze Grafana

Percorso:

```text
http://localhost:3000
```

Cosa cercare:

- pannelli su traffico;
- pannelli su errori;
- pannelli su latenza;
- confronto frontend/backend;
- alert o soglie impostate in UD21.

Screenshot/annotazione consigliata:

```text
Grafana mostra chiaramente il trend temporale,
ma dipende dalla qualità delle metriche esposte e dalla configurazione Prometheus.
```

## 3. Evidenze Azure Application Insights / Log Analytics

Percorso:

```text
Azure Portal -> Application Insights -> Logs
```

Query requests:

```kql
requests
| where timestamp > ago(30m)
| where url has "/products"
| summarize requests=count(), avgDurationMs=avg(duration), p95Duration=percentile(duration, 95) by name, resultCode
| order by requests desc
```

Query dependencies:

```kql
dependencies
| where timestamp > ago(30m)
| where name has "products" or target has "backend"
| project timestamp, name, target, resultCode, duration
| order by timestamp desc
```

Query exceptions:

```kql
exceptions
| where timestamp > ago(30m)
| project timestamp, type, outerMessage, operation_Id
| order by timestamp desc
```

Query log ACA:

```kql
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(30m)
| where Log_s has "products"
| project TimeGenerated, ContainerAppName_s, Log_s
| order by TimeGenerated desc
```

## 4. Esercizio Kibana-like su log JSON

Il file log è:

```text
UD23/data/logs/products_logs_sample.jsonl
```

Comandi:

```bash
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --summary
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --status-min 500
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --group-by path
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --contains slow
```

Interpretazione:

| Operazione simulata | Analogia log stack |
|---|---|
| filtro status >= 500 | query log errori |
| group-by path | aggregazione per campo |
| contains slow | ricerca testuale/pattern |
| summary | dashboard log minimale |


## 5. Evidenza Dynatrace Playground

Segui `10_OBS_UD23_DEMO_GUIDATA_Dynatrace_Playground_v6_0.md`.

Raccogli almeno:

| Evidenza | Cosa dimostra |
|---|---|
| service health / performance | vista centrata sul servizio |
| endpoint | granularità per operazione/request |
| infrastructure | correlazione servizio-risorsa |
| log o trace | passaggio contestuale tra segnali |
| relazione tra servizi | dipendenze/service flow |

Non confondere questa attività con una installazione Dynatrace: è una esplorazione pratica del Playground.

## 6. Compilazione matrice strumenti

Criteri consigliati:

| Criterio | Significato |
|---|---|
| effort iniziale | quanto è difficile avviarlo |
| ingestion | come entrano i dati |
| retention | quanto costa conservare dati |
| APM | capacità di vedere servizi/dipendenze |
| log search | capacità di ricerca log |
| alerting | capacità di generare allarmi |
| infra monitoring | host, servizi, trigger |
| vendor lock-in | dipendenza da cloud/vendor |
| adatto a | DevOps/SRE/IT Ops/Enterprise |

## 7. Errori tipici

### Errore: confronto superficiale

Sintomo:

```text
Grafana è meglio perché è più bella.
```

Correzione:

```text
Grafana è efficace per dashboard di metriche e alerting,
ma per log search strutturato serve uno stack log o Log Analytics.
```

### Errore: confondere log e metriche

Metriche:

```text
serie temporali numeriche aggregate
```

Log:

```text
eventi dettagliati, spesso testuali o JSON
```

### Errore: confondere Playground con installazione/configurazione

Per Dynatrace è corretto scrivere:

```text
Esplorazione pratica guidata nel Playground.
```

Non è corretto scrivere:

```text
Ho installato e configurato Dynatrace/OneAgent.
```

### Errore: trattare gli altri strumenti non installati come evidenze pratiche

Se uno strumento non è stato installato, scrivere:

```text
Valutazione basata su scheda strumento e caso d'uso.
```

Non scrivere che è stato provato.

## 8. Checklist finale

```text
[ ] Ho raccolto almeno una evidenza Prometheus/Grafana.
[ ] Ho raccolto almeno una evidenza Azure KQL/Application Insights.
[ ] Ho usato il log-stack simulato.
[ ] Ho completato la demo pratica Dynatrace Playground.
[ ] Ho compilato la matrice strumenti.
[ ] Ho distinto strumenti usati direttamente, Dynatrace esplorato in Playground e strumenti discussi solo tramite scheda.
[ ] Ho prodotto un report comparativo motivato.
```
