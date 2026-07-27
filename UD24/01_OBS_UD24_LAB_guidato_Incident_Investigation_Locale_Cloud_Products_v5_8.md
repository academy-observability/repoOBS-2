# OBS UD24 — Laboratorio guidato
# Incident investigation locale/cloud su app Catalogo prodotti

## 0. Scenario

Il team riceve una segnalazione:

> Alcuni utenti vedono lentezza o errore durante la consultazione del catalogo prodotti.

La richiesta non dice ancora se il problema sia nel frontend, nel backend, nella piattaforma cloud o nella rete applicativa. Il nostro compito è investigare usando segnali locali e cloud.

## 1. Prerequisiti

Devono essere disponibili:

- stack locale UD18–UD22 avviabile;
- frontend/backend products locali;
- Prometheus locale;
- Grafana locale;
- Jaeger locale;
- app products rilasciata su Azure Container Apps;
- Application Insights e Log Analytics collegati;
- query UD23 funzionanti;
- Azure CLI configurata;
- FQDN pubblico del frontend ACA.

Annotiamo i dati:

| Dato | Valore |
|---|---|
| Frontend locale | `http://localhost:8118` o porta usata nella tua UD |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |
| Jaeger | `http://localhost:16686` |
| Frontend ACA URL | |
| Resource Group | |
| Container App frontend | |
| Container App backend | |
| Log Analytics Workspace | |

## 2. Preparazione cartella evidenze

Dalla radice del repository:

```bash
mkdir -p work/UD24/evidence work/UD24/logs work/UD24/img
cp UD24/docs/template_incident_report_ud24.md work/UD24/evidence/incident_report_ud24.md 2>/dev/null || true
```

Se stiamo lavorando direttamente nel pacchetto UD24, copiamo manualmente i template dalla cartella `docs`.

## 3. Caso 1 — comportamento normale

Prima di generare problemi, raccogliamo una baseline rapida.

### 3.1 Traffico locale normale

```bash
bash UD24/scripts/generate_local_incident_traffic_ud24.sh normal http://localhost:8118
```

Se la porta del frontend locale è diversa, sostituiamo l'URL.

### 3.2 Verifica locale con curl

```bash
curl -i http://localhost:8118/products
curl -i http://localhost:8118/ready
```

Risultato atteso:

```text
HTTP 200
catalogo prodotti presente
backend raggiungibile
```

### 3.3 Prometheus

Apriamo Prometheus e proviamo:

```promql
up
```

Poi una query di traffico:

```promql
sum(rate(http_requests_total{path=~"/products|/api/products"}[2m])) by (service, path, status)
```

Annotiamo se frontend e backend stanno ricevendo richieste.

### 3.4 Grafana

Apriamo la dashboard costruita in UD20/UD21 e verifichiamo:

- request rate;
- error rate;
- latenza;
- target up.

### 3.5 Jaeger

Apriamo Jaeger:

```text
http://localhost:16686
```

Cerchiamo trace su `frontend-products` o nome servizio equivalente. Dobbiamo trovare un trace FE→BE per `/products`.

## 4. Caso 2 — lentezza controllata

### 4.1 Generare lentezza locale

```bash
bash UD24/scripts/generate_local_incident_traffic_ud24.sh slow http://localhost:8118
```

Oppure manualmente:

```bash
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://localhost:8118/products/slow
done
```

### 4.2 Osservare Prometheus/Grafana

Query candidata:

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{path=~"/products/slow|/api/products/slow"}[5m])) by (le, service, path))
```

Se l'app espone metriche con nomi diversi, usare la pagina `/metrics` per individuare il nome reale.

Domande:

- La latenza cresce solo su `/products/slow`?
- Cresce sia su frontend sia su backend?
- Il tasso errori resta basso?
- Jaeger mostra uno span backend più lungo?

### 4.3 Generare lentezza cloud

Impostiamo l'URL del frontend ACA:

```bash
export FRONTEND_URL="https://INSERISCI_FRONTEND_ACA"
bash UD24/scripts/generate_cloud_incident_traffic_ud24.sh slow "$FRONTEND_URL"
```

### 4.4 Query KQL per lentezza

In Log Analytics / Application Insights:

```kql
AppRequests
| where TimeGenerated > ago(30m)
| where Url has "/products/slow" or Name has "products/slow"
| summarize richieste=count(), durata_media_ms=avg(DurationMs), p95_ms=percentile(DurationMs, 95) by bin(TimeGenerated, 5m), ResultCode
| order by TimeGenerated asc
```

Poi:

```kql
AppDependencies
| where TimeGenerated > ago(30m)
| where Name has "products" or Target has "backend"
| summarize chiamate=count(), durata_media_ms=avg(DurationMs), p95_ms=percentile(DurationMs, 95) by bin(TimeGenerated, 5m), ResultCode
| order by TimeGenerated asc
```

Interpretazione attesa:

```text
Se requests frontend e dependencies verso backend mostrano latenza elevata,
il problema è probabilmente lungo la chiamata FE→BE o nel backend.
```

## 5. Caso 3 — errore controllato

### 5.1 Generare errore locale

```bash
bash UD24/scripts/generate_local_incident_traffic_ud24.sh error http://localhost:8118
```

Oppure:

```bash
curl -i http://localhost:8118/products/error
```

Risultato atteso:

```text
HTTP 500 o risposta di errore controllata
```

### 5.2 Prometheus/Grafana

Query error rate:

```promql
sum(rate(http_requests_total{status=~"5..", path=~"/products/error|/api/products/error"}[2m])) by (service, path, status)
```

Verifichiamo se l'errore appare su frontend, backend o entrambi.

### 5.3 Jaeger

Cerchiamo un trace relativo a `/products/error`.

Annotiamo:

| Campo | Valore |
|---|---|
| servizio frontend | |
| servizio backend | |
| status frontend | |
| status backend | |
| span più significativo | |
| eventuale errore annotato | |

### 5.4 Generare errore cloud

```bash
export FRONTEND_URL="https://INSERISCI_FRONTEND_ACA"
bash UD24/scripts/generate_cloud_incident_traffic_ud24.sh error "$FRONTEND_URL"
```

### 5.5 Query KQL per errori

```kql
AppRequests
| where TimeGenerated > ago(30m)
| where Url has "/products/error" or Name has "products/error"
| project TimeGenerated, Name, Url, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

```kql
AppExceptions
| where TimeGenerated > ago(30m)
| project TimeGenerated, Type, Message, OperationId, AppRoleName
| order by TimeGenerated desc
```

```kql
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(30m)
| where Log_s has "products/error" or Log_s has "request_id" or Log_s has "ERROR"
| project TimeGenerated, ContainerAppName_s, RevisionName_s, Log_s
| order by TimeGenerated desc
```

## 6. Costruzione della timeline

Usiamo il template:

```text
UD24/docs/template_timeline_ud24.md
```

La timeline deve distinguere:

- generazione traffico;
- rilevazione metrica;
- rilevazione log;
- rilevazione trace;
- query cloud;
- decisione tecnica.

Esempio:

| Ora | Evento | Fonte |
|---|---|---|
| 10:05 | baseline normale `/products` | curl/Grafana |
| 10:10 | traffico lento `/products/slow` | script |
| 10:12 | p95 aumenta | Grafana/PromQL |
| 10:14 | AppRequests mostra DurationMs elevato | KQL |
| 10:17 | Jaeger mostra span backend lento | Jaeger |

## 7. Formulazione ipotesi

Compiliamo una tabella:

| Ipotesi | Segnali a favore | Segnali contro | Stato |
|---|---|---|---|
| Frontend non raggiunge backend | `/ready` fallisce | backend health OK | da verificare |
| Backend lento | dependency lenta, span backend lungo | error rate basso | probabile |
| Errore applicativo backend | ResultCode 500 e log backend | piattaforma stabile | probabile |
| Problema piattaforma ACA | revision unhealthy | log applicativi normali | non confermata |

## 8. Incident report

Compiliamo:

```text
UD24/docs/template_incident_report_ud24.md
```

Il report deve includere:

- sintomo;
- impatto;
- timeline;
- segnali raccolti;
- ipotesi;
- root cause probabile;
- azione correttiva;
- limiti dell'analisi;
- follow-up.

## 9. Decisione correttiva

Le azioni possibili dipendono dallo scenario:

| Scenario | Azione plausibile |
|---|---|
| errore controllato endpoint backend | correggere codice backend o disabilitare endpoint problematico |
| latenza backend | ottimizzare logica backend, aumentare timeout, misurare dipendenza |
| frontend configurato male | correggere `BACKEND_URL` |
| revisione ACA non sana | rollback a revisione precedente |
| telemetria mancante | correggere connection string o strumentazione |

## 10. Commit evidenze

```bash
git add work/UD24/evidence work/UD24/logs work/UD24/img
git commit -m "UD24 - incident investigation locale cloud prodotti"
git push
```

Se il repository usato in aula non richiede commit delle evidenze, consegnare comunque i file compilati.

## 11. Chiusura

Il partecipante deve saper spiegare:

> Ho distinto comportamento normale, lento ed errore. Ho raccolto segnali locali e cloud. Ho collegato metriche, log e trace. Ho prodotto una timeline e una root cause probabile, indicando anche i limiti dell'analisi.
