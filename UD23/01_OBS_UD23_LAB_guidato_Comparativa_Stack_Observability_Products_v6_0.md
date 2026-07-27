# OBS UD23 - Laboratorio guidato
# Comparativa stack Observability sulla app Catalogo prodotti

## 0. Obiettivo del laboratorio

In questo laboratorio osserviamo la stessa app, **Catalogo prodotti**, da più prospettive. Non installiamo nuovi strumenti pesanti in aula. Usiamo gli strumenti già disponibili, un piccolo esercizio log-stack simulato e una **demo hands-on su Dynatrace Playground** per osservare concretamente una piattaforma enterprise APM/Observability senza installare agenti.

L'obiettivo finale è produrre un report comparativo tecnico, non una classifica soggettiva.

```text
Stessa app
stesso traffico
stessi scenari /products /products/slow /products/error
più viste di osservabilità
report comparativo finale
```

## 1. Prerequisiti

Devono essere disponibili almeno:

| Elemento | Provenienza |
|---|---|
| App Catalogo prodotti locale | UD18-UD22 |
| Prometheus locale | UD19 |
| Grafana locale | UD20-UD21 |
| Jaeger/log locali | UD22 |
| App Catalogo prodotti su Azure Container Apps | UD16/UD17 |
| Application Insights + Log Analytics | UD17 |
| Query KQL base | UD17/UD23 |
| Dataset log-stack simulato | questa UD |

## 2. Preparazione cartella evidenze

Dalla radice del repository:

```bash
mkdir -p work/UD23/docs
mkdir -p work/UD23/evidence
mkdir -p work/UD23/logs
```

Copia i template forniti dalla UD:

```bash
cp UD23/docs/templates/report_comparativo_template.md work/UD23/docs/report_comparativo_observability_ud23.md
cp UD23/docs/templates/tooling_matrix_template.md work/UD23/docs/tooling_matrix_ud23.md
cp UD23/docs/templates/evidence_template_ud23.md work/UD23/docs/evidence_ud23.md
```

## 3. Generazione traffico coerente

Usiamo tre comportamenti applicativi:

```text
/products        -> comportamento normale
/products/slow   -> lentezza controllata
/products/error  -> errore controllato
```

Se lavori sullo stack locale, apri un terminale e genera traffico verso il frontend locale:

```bash
FRONTEND_LOCAL="http://localhost:8080"

for i in {1..10}; do curl -s "$FRONTEND_LOCAL/products" > /dev/null; done
for i in {1..3};  do curl -s "$FRONTEND_LOCAL/products/slow" > /dev/null; done
for i in {1..3};  do curl -s "$FRONTEND_LOCAL/products/error" > /dev/null || true; done
```

Se lavori sul cloud, sostituisci l'URL:

```bash
FRONTEND_CLOUD="https://<frontend-aca-url>"

for i in {1..10}; do curl -s "$FRONTEND_CLOUD/products" > /dev/null; done
for i in {1..3};  do curl -s "$FRONTEND_CLOUD/products/slow" > /dev/null; done
for i in {1..3};  do curl -s "$FRONTEND_CLOUD/products/error" > /dev/null || true; done
```

## 4. Vista Prometheus/Grafana

Apri Prometheus:

```text
http://localhost:9090
```

Esegui query di verifica:

```promql
up
```

Poi usa query legate all'app, adattando il nome delle metriche se nel tuo stack è diverso:

```promql
sum(rate(http_requests_total[5m])) by (service, path)
```

```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, path)
```

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service, path))
```

Apri Grafana:

```text
http://localhost:3000
```

Raccogli evidenze:

| Evidenza | Cosa annotare |
|---|---|
| pannello request rate | endpoint più chiamati |
| pannello error rate | presenza di `/products/error` |
| pannello latency/p95 | differenza tra `/products` e `/products/slow` |
| target status | frontend/backend UP |

## 5. Vista Azure Monitor / Application Insights

Apri:

```text
Azure Portal -> Application Insights -> Logs
```

Usa le query fornite in `UD23/kql/products_comparativa.kql`.

Query base:

```kql
requests
| where timestamp > ago(30m)
| where url has "/products"
| summarize requests=count(), avgDurationMs=avg(duration) by name, resultCode
| order by requests desc
```

Dipendenze FE -> BE:

```kql
dependencies
| where timestamp > ago(30m)
| where name has "products" or target has "backend"
| project timestamp, name, target, resultCode, duration
| order by timestamp desc
```

Log container ACA:

```kql
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(30m)
| where Log_s has "products"
| project TimeGenerated, ContainerAppName_s, Log_s
| order by TimeGenerated desc
```

Raccogli evidenze:

| Evidenza | Cosa annotare |
|---|---|
| requests | conteggi e durate per endpoint |
| dependencies | relazione frontend/backend |
| traces/log | messaggi applicativi |
| ContainerAppConsoleLogs | comportamento runtime container |

## 6. Vista log-stack Kibana-like simulata

Non installiamo ELK completo in questo laboratorio. Usiamo un dataset JSONL e uno script Python per simulare le operazioni minime che faremmo in uno stack log: filtrare, cercare, raggruppare, contare errori.

Esegui:

```bash
python3 UD23/tools/logstack_kibana_like/query_logs.py \
  --file UD23/data/logs/products_logs_sample.jsonl \
  --summary
```

Filtra gli errori:

```bash
python3 UD23/tools/logstack_kibana_like/query_logs.py \
  --file UD23/data/logs/products_logs_sample.jsonl \
  --status-min 500
```

Raggruppa per endpoint:

```bash
python3 UD23/tools/logstack_kibana_like/query_logs.py \
  --file UD23/data/logs/products_logs_sample.jsonl \
  --group-by path
```

Cerca lentezza:

```bash
python3 UD23/tools/logstack_kibana_like/query_logs.py \
  --file UD23/data/logs/products_logs_sample.jsonl \
  --contains slow
```

Annota nel report:

```text
Cosa ho trovato più facilmente nei log rispetto alle metriche?
Cosa non posso capire dai soli log?
Quali campi sono indispensabili per rendere utile il log search?
```

## 7. Demo pratica Dynatrace Playground

Esegui il file:

```text
10_OBS_UD23_DEMO_GUIDATA_Dynatrace_Playground_v6_0.md
```

Questa parte è pratica: devi navigare almeno un servizio, osservare indicatori, endpoint, infrastruttura e una relazione/log/trace disponibile. Registra l'evidenza nel file `work/UD23/docs/evidence_ud23.md`.

**Non è richiesta l'installazione di OneAgent.**

## 8. Schede strumenti enterprise

Apri:

```text
06_OBS_UD23_SCHEDE_STRUMENTI_Enterprise_Monitoring_v6_0.md
```

Non devi installare Zabbix, Splunk o OpenText. Dynatrace viene invece esplorato nel Playground; la sua scheda serve a consolidare posizionamento, casi d'uso e limiti.

Per ogni strumento indica:

```text
1 caso d'uso adatto
1 limite
1 condizione in cui lo valuteresti
```

## 9. Compilazione matrice comparativa

Apri:

```text
work/UD23/docs/tooling_matrix_ud23.md
```

Compila almeno queste righe:

| Strumento/stack | Segnale forte | Limite | Quando usarlo |
|---|---|---|---|
| Prometheus/Grafana | | | |
| Azure Monitor/App Insights | | | |
| Log Analytics/KQL | | | |
| Kibana-like/log stack | | | |
| Zabbix | | | |
| Splunk | | | |
| Dynatrace | | | |
| OpenText | | | |

## 10. Report comparativo finale

Apri:

```text
work/UD23/docs/report_comparativo_observability_ud23.md
```

Il report deve contenere:

1. scenario osservato;
2. stack confrontati;
3. evidenze raccolte;
4. differenze tra metriche, log, trace, APM;
5. matrice criteri;
6. scelta consigliata per un team piccolo;
7. scelta consigliata per ambiente enterprise;
8. limiti della comparativa.

## 11. Criterio di completamento

Il laboratorio è completo quando puoi dire:

```text
Ho osservato la stessa app da più viste.
So spiegare cosa vedo meglio con Prometheus/Grafana,
cosa vedo meglio con Application Insights/KQL,
e quando avrebbe senso valutare uno stack log o uno strumento enterprise.
Ho inoltre esplorato direttamente Dynatrace Playground e so descrivere cosa integra rispetto a Prometheus/Grafana e Jaeger.
```
