# OBS UD23 - Mini-attività
# Mappa strumenti, segnali e casi d'uso Observability

## Obiettivo

Questa mini-attività serve a evitare una confusione frequente: pensare che tutti gli strumenti di monitoraggio facciano la stessa cosa. In realtà alcuni sono più forti sulle metriche, altri sui log, altri sull'APM, altri sull'infrastruttura o su contesti enterprise.

## Attività 1 - Mappa domanda/strumento

Completa la tabella.

| Domanda operativa | Strumento/stack candidato | Perché |
|---|---|---|
| Il frontend è UP? | | |
| Il backend è UP? | | |
| `/products/slow` ha p95 più alto? | | |
| Dove vedo la relazione FE -> BE? | | |
| Voglio cercare tutti i log con `request_id=...` | | |
| Devo controllare host e servizi tradizionali | | |
| Devo fare APM enterprise con service map automatica | | |
| Devo confrontare costi e retention dei log | | |

## Attività 2 - Pro/contro controllato

Per ciascuno, indica un punto forte e un limite.

| Strumento/stack | Punto forte | Limite |
|---|---|---|
| Prometheus/Grafana | | |
| Application Insights/Azure Monitor | | |
| Log Analytics/KQL | | |
| Kibana-like/log stack | | |
| Zabbix | | |
| Splunk | | |
| Dynatrace | | |
| OpenText | | |

## Attività 3 - Decisione sintetica

Scenario:

```text
Una PMI ha una app containerizzata su Azure, un team piccolo e necessità di dashboard e alert su errori/latenza.
```

Quale stack proporresti per partire? Motiva in 5-7 righe.

Scenario:

```text
Una grande azienda ha applicazioni ibride, molti sistemi legacy, bisogno di log retention lunga,
processi ITSM e APM enterprise.
```

Quali strumenti valuteresti e perché? Motiva in 5-7 righe.
