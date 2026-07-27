# Report comparativo Observability - UD23

## 1. Scenario

App osservata: Catalogo prodotti.
Endpoint considerati: `/products`, `/products/slow`, `/products/error`.

## 2. Stack confrontati

| Stack | Usato direttamente? | Tipo evidenza |
|---|---|---|
| Prometheus/Grafana | sì | metriche/dashboard |
| Application Insights/Log Analytics | sì | richieste/dipendenze/log cloud |
| Log stack Kibana-like | simulato | log JSON/filter/group-by |
| Zabbix | scheda | infrastruttura |
| Splunk | scheda | log/eventi enterprise |
| Dynatrace | **sì, Playground** | APM enterprise / servizi / dipendenze / log / trace |
| OpenText | scheda | ITOM/AIOps enterprise |

## 3. Evidenze raccolte

### Prometheus/Grafana

### Application Insights / KQL

### Log stack simulato

### Dynatrace Playground


## 4. Confronto per segnale

| Segnale | Stack più adatto | Motivo |
|---|---|---|
| request rate | | |
| error rate | | |
| p95 latency | | |
| log search | | |
| FE -> BE dependency | | |
| service-centric navigation | | |
| infrastructure trigger | | |

## 5. Confronto per criteri operativi

| Criterio | Nota |
|---|---|
| effort iniziale | |
| costi/retention | |
| profondità APM | |
| integrazione Azure | |
| scalabilità enterprise | |

## 6. Raccomandazione finale

## 7. Limiti della comparativa
