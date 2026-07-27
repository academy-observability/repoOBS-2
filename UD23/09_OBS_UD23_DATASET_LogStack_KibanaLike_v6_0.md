# OBS UD23 - Dataset log-stack Kibana-like

## Scopo

Questo file spiega il dataset usato per simulare una piccola esperienza di log search tipo Kibana senza installare Elastic Stack.

Il dataset è:

```text
UD23/data/logs/products_logs_sample.jsonl
```

Ogni riga è un evento JSON con campi:

```text
timestamp
service
level
message
request_id
path
status
latency_ms
trace_id
span_id
```

## Perché non installiamo ELK completo

ELK/Kibana è uno stack potente, ma può richiedere memoria, configurazione e tempo. In questa UD l'obiettivo non è amministrare Elastic, ma capire la funzione di uno stack log: indicizzare, filtrare, raggruppare e visualizzare eventi.

Per questo usiamo una simulazione controllata, con dataset e script già forniti.

## Comandi principali

```bash
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --summary
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --status-min 500
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --group-by path
python3 UD23/tools/logstack_kibana_like/query_logs.py --file UD23/data/logs/products_logs_sample.jsonl --contains slow
```
