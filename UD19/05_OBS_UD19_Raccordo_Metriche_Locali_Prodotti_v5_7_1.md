# OBS UD19 — Raccordo finale
# Dalle metriche grezze alle dashboard operative

In UD19 abbiamo imparato a interrogare direttamente Prometheus. Questo passaggio è volutamente tecnico: prima di costruire dashboard dobbiamo sapere da dove arrivano i numeri e che cosa significano.

La progressione ora è naturale:

```text
UD19: Prometheus raccoglie e interroghiamo metriche
UD20: Grafana trasforma le query in pannelli leggibili
UD21: alcune query diventano condizioni di alert
UD22: metriche, log e trace vengono correlate
```

Il punto da conservare è questo: una dashboard non è una decorazione grafica. Una buona dashboard nasce da query che abbiamo già compreso. Se non capiamo `rate`, `status`, `path`, `service` e latenza, i pannelli Grafana diventano solo immagini.

Per questo UD19 è il fondamento operativo di UD20 e UD21.
