# OBS UD21 — Laboratorio autonomo
# Alert di latenza p95 con notifica webhook

## Obiettivo

Creare una seconda regola Grafana-managed che rilevi un degrado persistente della latenza user-facing del frontend e notifichi lo stesso receiver webhook.

---

## Vincoli

La regola deve usare:

- metrica histogram `app_http_request_duration_seconds_bucket`;
- punto di vista `products-frontend`;
- path `/products.*`;
- percentile p95;
- query di tipo `Instant`;
- expression Threshold separata;
- soglia didattica `1.5` secondi;
- evaluation group `ud21-every-30s`;
- pending period `1m`;
- contact point `UD21 - Webhook locale`;
- labels `service`, `severity`, `ud`, `signal`;
- annotazione con riferimento al runbook.

Query di partenza:

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

---

## Procedura richiesta

1. Generare baseline normale.
2. Verificare la query in Prometheus.
3. Creare la query A in Grafana.
4. Creare B con `A IS ABOVE 1.5`.
5. Impostare B come alert condition.
6. Configurare folder, evaluation group e pending period.
7. Collegare il webhook.
8. Generare traffico lento:

```bash
DURATION_SECONDS=180 ./scripts/generate_latency_condition_ud21.sh
```

9. Osservare `Pending`, `Alerting/Firing`, payload `firing`.
10. Tornare al traffico normale e osservare il `resolved`.
11. Individuare in Jaeger almeno una trace lenta.
12. Fermare e riavviare lo stack senza `-v` e verificare che la regola esista ancora.

---

## Domande di analisi

1. Perché il p95 è più adatto della media a evidenziare la coda lenta?
2. Perché `sum by (le)` è necessario per `histogram_quantile`?
3. Quante alert instance produce questa query e perché?
4. Quale differenza c'è tra latenza del frontend e tempo trascorso nel backend?
5. Il payload webhook contiene una causa o un sintomo?
6. Quale volume conserva la regola?
7. Le trace Jaeger sopravvivono alla ricreazione del container? Motivare.

---

## Evidenze obbligatorie

- query A e threshold B;
- stato `Alerting/Firing`;
- payload webhook `firing`;
- payload webhook `resolved`;
- pannello p95;
- trace lenta Jaeger;
- prova della persistenza della regola;
- runbook compilato.
