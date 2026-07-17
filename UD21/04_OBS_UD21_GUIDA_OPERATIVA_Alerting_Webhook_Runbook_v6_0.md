# OBS UD21 — Guida operativa e troubleshooting
# Grafana Alerting 11.3, webhook locale, soglie e runbook

## 1. Avvio e verifica stack

```bash
cd UD21/src/app_products_alerting
./scripts/start_stack_ud21.sh
```

Controllare:

```bash
docker compose ps
curl -s http://localhost:8121/health
curl -s http://localhost:9090/-/ready
curl -s http://localhost:5001/health
```

Aprire:

```text
Grafana:          http://localhost:3000
Prometheus:       http://localhost:9090
Webhook events:  http://localhost:5001/events
Jaeger:           http://localhost:16686
```

---

## 2. Generare una baseline senza errori

```bash
./scripts/generate_traffic_ud21.sh
```

Il traffico baseline usa `/`, `/products` e `/ready`; non chiama gli endpoint controllati `/products/error` e `/products/slow`.

Verificare in Prometheus:

```promql
up{job=~"products-.*"}
```

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{path=~"/(api/)?products.*"}[1m])
)
```

---

## 3. Query robusta dell'error rate

Usare questa query sia in Prometheus sia nella query A della regola:

```promql
(
  sum(
    rate(
      app_http_requests_total{
        service="products-frontend",
        path=~"/products.*",
        status=~"5.."
      }[2m]
    )
  ) or vector(0)
)
/
clamp_min(
  sum(
    rate(
      app_http_requests_total{
        service="products-frontend",
        path=~"/products.*"
      }[2m]
    )
  ) or vector(0),
  0.001
)
```

Valore atteso in baseline:

```text
0 o valore molto vicino a 0
```

---

## 4. Creazione del contact point webhook

Percorso Grafana:

```text
Alerts & IRM
→ Alerting
→ Contact points
→ Add contact point
```

Valori:

| Campo | Valore |
|---|---|
| Name | `UD21 - Webhook locale` |
| Integration | `Webhook` |
| URL | `http://webhook-receiver:5001/grafana-alert` |
| HTTP method | `POST` |
| Disable resolved message | lasciare disabilitato |

Premere `Test`, inviare la test notification e verificare:

```text
http://localhost:5001/events
```

Solo dopo il test positivo salvare il contact point.

### Errore: connection refused

```bash
docker compose ps webhook-receiver
docker logs ud21-webhook-receiver --tail 100
```

### Errore: URL con localhost

Correggere:

```text
ERRATO  http://localhost:5001/grafana-alert
CORRETTO http://webhook-receiver:5001/grafana-alert
```

---

## 5. Creazione completa della regola error rate

Percorso:

```text
Alerts & IRM
→ Alerting
→ Alert rules
→ New alert rule
```

### 5.1 Nome e tipo

```text
Rule name: UD21 - Products high error rate
Rule type: Grafana-managed alert
```

### 5.2 Query A

- datasource: `Prometheus`;
- incollare la query robusta;
- `Type`: `Instant`;
- premere `Run queries`.

Il risultato deve essere un numero. Non procedere se compare `NaN`.

### 5.3 Expression B

Sotto la query:

```text
Add expression
→ Threshold
```

Impostare:

```text
Input: A
IS ABOVE: 0.20
```

Premere `Set as alert condition` sull'espressione B. Il badge verde deve trovarsi su B, non su A.

Risultato atteso in baseline:

```text
B = 0
Normal
```

### 5.4 Evaluation behavior

Creare o selezionare:

```text
Folder: UD21
Evaluation group: ud21-every-30s
Evaluation interval: 30s
Pending period: 1m
```

Lasciare i comportamenti `No Data` ed `Error` ai valori predefiniti della piattaforma per il laboratorio; annotare comunque che sono stati distinti dalla condizione normale.

### 5.5 Labels e annotations

Labels:

```text
service=products-frontend
severity=warning
ud=UD21
signal=error-rate
```

Annotations:

```text
summary=Error rate elevato sugli endpoint products
```

```text
description=Il rapporto 5xx sul frontend products è superiore al 20% per almeno 1 minuto. Verificare dashboard, PromQL, log frontend/backend e trace Jaeger.
```

```text
runbook=templates/runbook-alert-prodotti-ud21.md
```

### 5.6 Notifications

Nella sezione notifiche scegliere:

```text
Select contact point
→ UD21 - Webhook locale
```

Salvare con `Save rule and exit`.

---

## 6. Generare il firing

Aprire un secondo terminale:

```bash
DURATION_SECONDS=180 ./scripts/generate_alert_condition_ud21.sh
```

Osservare:

```text
Normal → Pending → Alerting/Firing
```

Poi aprire:

```text
http://localhost:5001/events
```

Cercare un evento con:

```json
{"status": "firing"}
```

---

## 7. Generare e osservare il resolved

Dopo la fine del burst di errori, generare solo traffico normale:

```bash
DURATION_SECONDS=180 ./scripts/generate_traffic_ud21.sh
```

Attendere che la finestra `[2m]` non contenga più una quota superiore al 20% di errori. La regola deve tornare `Normal` e il receiver deve ricevere:

```json
{"status": "resolved"}
```

La transizione può richiedere più di due minuti perché dipende da finestra PromQL, evaluation interval e tempi di notifica.

---

## 8. Alert di latenza p95

Query consigliata:

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(
      app_http_request_duration_seconds_bucket{
        service="products-frontend",
        path=~"/products.*"
      }[2m]
    )
  )
)
```

Configurazione:

```text
Query A: Instant
Expression B: A IS ABOVE 1.5
Alert condition: B
Evaluation group: ud21-every-30s
Pending period: 1m
Contact point: UD21 - Webhook locale
```

Traffico lento:

```bash
DURATION_SECONDS=180 ./scripts/generate_latency_condition_ud21.sh
```

Questo secondo alert è svolto nel laboratorio autonomo o come estensione del guidato.

---

## 9. Diagnosi con log e trace

Errori:

```bash
docker logs ud21-products-frontend --tail 150
docker logs ud21-products-backend --tail 150
```

Latenza:

```text
Jaeger
→ Service products-frontend o products-backend
→ Find Traces
```

Cercare richieste `/products/slow` e `/api/products/slow`.

---

## 10. Troubleshooting sistematico

### Query A restituisce `NaN`

Cause:

- è stata usata la query semplice con divisione `0/0`;
- la query robusta è stata copiata parzialmente.

Soluzione: usare `or vector(0)` e `clamp_min` come nel template.

### B è vera ma la regola non passa in Alerting

Verificare:

- il badge `Alert condition` è su B;
- il pending period è realmente `1m`;
- il burst dura abbastanza;
- l'evaluation group valuta ogni `30s`;
- il valore A resta sopra `0.20`.

### La regola è Alerting ma non arriva il webhook

Verificare:

- contact point selezionato nella regola;
- test del contact point riuscito;
- URL con nome servizio Docker;
- log Grafana e receiver;
- resolved messages non disabilitati.

### La regola è sparita dopo il riavvio

Verificare:

```bash
docker inspect ud21-grafana \
  --format '{{range .Mounts}}{{println .Name .Destination}}{{end}}'
```

Deve comparire:

```text
obs-ud21-grafana-data /var/lib/grafana
```

### Prometheus ha perso la cronologia

Verificare il mount:

```text
obs-ud21-prometheus-data /prometheus
```

Controllare di non aver eseguito `docker compose down -v`.

---

## 11. Arresto corretto

```bash
./scripts/stop_stack_ud21.sh
```

Questo conserva i volumi.

Reset solo quando richiesto:

```bash
RESET_UD21=yes ./scripts/reset_stack_ud21.sh
```
