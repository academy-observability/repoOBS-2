# OBS UD21 — Laboratorio guidato
# Alerting Grafana con contact point webhook e volumi persistenti

## Obiettivo

Costruire e verificare il ciclo completo:

```text
metriche → query A → threshold B → Pending → Alerting → webhook firing → resolved
```

Al termine verificheremo anche che regola, contact point e dati sopravvivano a un normale `docker compose down` grazie ai volumi.

---

## Task 1 — Avviare lo stack

```bash
cd UD21/src/app_products_alerting
./scripts/start_stack_ud21.sh
```

Verificare:

```bash
docker compose ps
```

Tutti i servizi devono essere `Up`; i servizi con healthcheck devono diventare `healthy`.

Aprire:

```text
Frontend:          http://localhost:8121
Prometheus:        http://localhost:9090
Grafana:           http://localhost:3000
Webhook receiver:  http://localhost:5001/events
Jaeger:            http://localhost:16686
```

Credenziali Grafana:

```text
admin / admin
```

---

## Task 2 — Verificare i volumi

```bash
./scripts/inspect_volumes_ud21.sh
```

Devono comparire:

```text
obs-ud21-grafana-data
obs-ud21-prometheus-data
obs-ud21-webhook-data
```

Annotare nel report:

| Volume | Mount point | Cosa conserva |
|---|---|---|
| Grafana | `/var/lib/grafana` | regole e contact point |
| Prometheus | `/prometheus` | serie temporali |
| Webhook | `/data` | payload ricevuti |

---

## Task 3 — Generare una baseline normale

```bash
./scripts/generate_traffic_ud21.sh
```

Aprire la dashboard:

```text
Dashboards
→ Academy Observability
→ UD21 - Catalogo prodotti - Alerting e webhook
```

Osservare:

- target frontend e backend `UP`;
- request rate;
- error rate user-facing vicino a zero;
- latenza p95 sotto la soglia didattica.

---

## Task 4 — Verificare la query dell'alert

In Prometheus eseguire la query robusta presente in:

```text
templates/promql-alert-rules-ud21.md
```

Il valore deve essere numerico e compreso tra `0` e `1`.

Domanda:

> Perché nella regola osserviamo `service="products-frontend"` invece di sommare frontend e backend?

Risposta da annotare: il frontend rappresenta il risultato user-facing; sommare entrambi potrebbe contare due volte la stessa richiesta distribuita.

---

## Task 5 — Creare e testare il contact point webhook

In Grafana:

```text
Alerts & IRM
→ Alerting
→ Contact points
→ Add contact point
```

Impostare:

```text
Name: UD21 - Webhook locale
Integration: Webhook
URL: http://webhook-receiver:5001/grafana-alert
HTTP method: POST
```

Non disabilitare i resolved messages.

Premere `Test` e inviare una test notification.

Aprire:

```text
http://localhost:5001/events
```

Risultato atteso: compare un evento di test. Salvare il contact point.

Domanda:

> Perché nella URL del contact point non usiamo `localhost`?

---

## Task 6 — Creare la query A

In Grafana:

```text
Alerts & IRM
→ Alerting
→ Alert rules
→ New alert rule
```

Impostare:

```text
Rule name: UD21 - Products high error rate
Rule type: Grafana-managed alert
Datasource: Prometheus
```

Incollare la query robusta del template e configurare:

```text
Ref ID: A
Type: Instant
```

Premere `Run queries`.

Risultato atteso:

```text
A restituisce un numero; in baseline è circa 0
```

Non procedere se compare `NaN`.

---

## Task 7 — Creare la condizione B

Sotto la query A:

```text
Add expression
→ Threshold
```

Impostare:

```text
Input: A
IS ABOVE: 0.20
```

Premere `Set as alert condition` su B.

Controllo visivo obbligatorio:

```text
il badge verde Alert condition deve trovarsi su B
```

In baseline il preview deve indicare condizione normale.

---

## Task 8 — Configurare evaluation behavior

Creare:

```text
Folder: UD21
Evaluation group: ud21-every-30s
Evaluation interval: 30s
Pending period: 1m
```

Spiegare a voce:

```text
30s = frequenza di valutazione
1m  = tempo minimo durante il quale la condizione deve restare vera
```

---

## Task 9 — Configurare labels, annotations e notifica

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

Nella sezione notifiche:

```text
Select contact point
→ UD21 - Webhook locale
```

Salvare la regola.

---

## Task 10 — Generare la condizione di errore

In un secondo terminale:

```bash
cd UD21/src/app_products_alerting
DURATION_SECONDS=180 ./scripts/generate_alert_condition_ud21.sh
```

Osservare nella pagina della regola:

```text
Normal → Pending → Alerting/Firing
```

Aprire il receiver:

```text
http://localhost:5001/events
```

Cercare un payload con stato `firing`.

Salvare screenshot di:

- valore A sopra `0.20`;
- expression B vera;
- stato `Pending` o `Alerting/Firing`;
- evento webhook `firing`.

---

## Task 11 — Diagnosi iniziale

Controllare i log:

```bash
docker logs ud21-products-frontend --tail 120
docker logs ud21-products-backend --tail 120
```

In Prometheus confrontare:

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{status=~"5.."}[1m])
)
```

Rispondere:

1. l'errore è visibile nel frontend, nel backend o in entrambi?
2. qual è il path frontend?
3. qual è il path backend corrispondente?
4. perché l'alert usa solo il punto di vista frontend?

---

## Task 12 — Osservare il resolved

Dopo il termine del burst, eseguire traffico normale:

```bash
DURATION_SECONDS=180 ./scripts/generate_traffic_ud21.sh
```

Attendere il rientro della finestra temporale.

Risultati attesi:

```text
Alerting/Firing → Normal
Webhook status=firing → webhook status=resolved
```

Il resolved può arrivare con ritardo rispetto alla fine dello script.

---

## Task 13 — Prova di persistenza

Arrestare senza eliminare i volumi:

```bash
./scripts/stop_stack_ud21.sh
```

Riavviare:

```bash
./scripts/start_stack_ud21.sh
```

Verificare che siano ancora presenti:

- contact point;
- alert rule;
- eventi webhook precedenti;
- cronologia Prometheus.

Spiegare perché la dashboard torna anche se è provisioned da file, mentre regola e contact point dipendono dal volume Grafana.

---

## Task 14 — Evidenze

Copiare il template:

```bash
mkdir -p ../../evidence
cp ../../docs/template_evidence_ud21.md ../../evidence/evidence_ud21.md
```

Compilare tutte le sezioni, inclusa la prova dei volumi.

---

## Task 15 — Arresto finale

```bash
./scripts/stop_stack_ud21.sh
```

Non usare `docker compose down -v`, salvo reset esplicito concordato con il docente.
