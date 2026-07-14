# OBS UD17 - Raccordo
# Dalla observability cloud allo stack locale

UD17 chiude il primo ciclo cloud completo: abbiamo una app FE/BE distribuita su Azure Container Apps, una release products tracciata da BuildId, telemetria applicativa verso Application Insights e log container interrogabili in Log Analytics.

Il valore di questa UD non è solo avere query KQL funzionanti. Il valore è avere un modo di pensare replicabile:

```text
richiesta utente
  ↓
frontend
  ↓
backend
  ↓
segnali osservabili
  ↓
interpretazione tecnica
  ↓
decisione
```

Nelle prossime UD ricostruiremo un ambiente locale controllato con lo stesso workload applicativo. Non sarà una copia di Azure: sarà un laboratorio in cui potremo vedere da vicino le componenti dello stack osservante.

```text
UD18 → app-stack products + obs-stack locale
UD19 → Prometheus raccoglie metriche FE/BE
UD20 → Grafana visualizza dashboard operative
UD21 → alerting locale su errori/latenza
UD22 → Jaeger, log e correlazione request/trace
```

La scelta di usare ancora il Catalogo prodotti è intenzionale. In cloud abbiamo osservato `/products`, `/products/slow` e `/products/error` con strumenti Azure. In locale li osserveremo con Prometheus, Grafana, Jaeger e log strutturati. Il partecipante potrà così confrontare due modi diversi di guardare lo stesso comportamento.

## Frase di raccordo

> In Azure ho usato servizi gestiti per osservare l'app products. Nel blocco locale userò uno stack esplicito, composto da strumenti containerizzati, per capire meglio cosa raccolgono metriche, log e trace.
