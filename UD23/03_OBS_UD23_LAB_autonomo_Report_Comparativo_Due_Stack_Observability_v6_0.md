# OBS UD23 - Laboratorio autonomo
# Report comparativo tra due stack Observability

## Scenario

Devi preparare un report per un responsabile tecnico che vuole capire quale stack usare per monitorare l'app **Catalogo prodotti**.

Non devi installare nuovi tool. Devi usare le evidenze raccolte nel laboratorio guidato, inclusa la demo Dynatrace Playground, e le schede strumenti fornite.

## Consegna

Produci il file:

```text
work/UD23/docs/report_comparativo_observability_ud23.md
```

Il report deve confrontare almeno due stack reali o simulati:

```text
Prometheus/Grafana
Azure Monitor/Application Insights/Log Analytics
Log stack Kibana-like simulato
```

Puoi includere Zabbix, Splunk, Dynatrace e OpenText nella matrice decisionale. Per Dynatrace puoi dichiarare l'esplorazione pratica del Playground, ma non una installazione/configurazione OneAgent; per Zabbix, Splunk e OpenText la valutazione resta basata sulle schede.

## Struttura minima

```markdown
# Report comparativo UD23

## Scenario

## Stack confrontati

## Evidenze raccolte

## Confronto per segnale

## Confronto per effort/costo/retention

## Quando userei uno stack rispetto all'altro

## Raccomandazione finale

## Limiti della comparativa
```

## Criteri di valutazione

| Criterio | Peso |
|---|---:|
| Uso di evidenze reali raccolte nel lab | alto |
| Chiarezza distinzione metriche/log/trace/APM | alto |
| Motivazione tecnica, non preferenza soggettiva | alto |
| Uso corretto delle schede strumenti | medio |
| Sintesi e leggibilità | medio |

## Nota importante

Non scrivere:

```text
Dynatrace è migliore perché è enterprise.
```

Scrivi invece:

```text
Dynatrace sarebbe da valutare in un contesto enterprise in cui servono APM, service flow,
automatic dependency mapping e analisi avanzata, ma nel nostro laboratorio non è stato installato.
La valutazione si basa quindi su scheda strumento e caso d'uso, non su evidenza pratica diretta.
```
