# OBS UD20 — Mini-attività
# Dashboard, pannelli e domande operative

Compila la tabella collegando ogni pannello a una domanda tecnica.

| Pannello | Query o metrica principale | Domanda operativa | Cosa mi aspetto dopo traffico normale/lento/errore |
|---|---|---|---|
| Target UP | `up{job=~"products-.*"}` | | |
| Request rate | `rate(app_http_requests_total[1m])` | | |
| Error rate | `status=~"5.."` | | |
| Latency p95 | `histogram_quantile(...)` | | |
| Average latency | `_sum / _count` | | |
| Total requests | `app_http_requests_total` | | |

## Domande brevi

1. Perché Grafana usa `http://prometheus:9090` e non `http://localhost:9090`?
2. Perché prima di analizzare una dashboard conviene controllare i target Prometheus?
3. Quale endpoint dovrebbe far crescere soprattutto la latenza?
4. Quale endpoint dovrebbe far crescere gli errori 5xx?
5. Una dashboard vuota significa sempre che l'applicazione non produce traffico?
6. Qual è la differenza tra pannello e query PromQL?
7. Che cosa controlleresti se il pannello error rate resta vuoto dopo `/products/error`?
