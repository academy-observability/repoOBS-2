# OBS UD18 — Raccordo finale
# Dal laboratorio locale ai prossimi strumenti di observability

In UD18 abbiamo costruito la base locale. Non abbiamo ancora sfruttato in profondità tutti gli strumenti, ma abbiamo ottenuto una cosa importante: un ambiente ripetibile in cui frontend e backend prodotti producono segnali osservabili.

La sequenza successiva diventa naturale:

```text
UD19 → Prometheus e PromQL
UD20 → Grafana e dashboard
UD21 → Alerting locale e runbook
UD22 → Jaeger, log e correlazione
```

Il valore del Catalogo prodotti è che rende gli esempi meno astratti. Una richiesta `/products` rappresenta un flusso normale; `/products/slow` rappresenta un degrado; `/products/error` rappresenta una condizione anomala. Questi tre casi saranno usati per costruire query, pannelli, alert e trace leggibili.

La frase da portare avanti è:

> In UD18 non abbiamo solo avviato dei container: abbiamo preparato un sistema osservabile locale in cui applicazione e strumenti sono separati ma collegati. Da questo momento possiamo analizzare metriche, log e trace su un workload coerente con quello cloud.
