# OBS UD21 — Alerting locale Grafana con webhook e persistenza

In UD19 abbiamo interrogato Prometheus. In UD20 abbiamo costruito dashboard Grafana. In UD21 trasformiamo le metriche in segnali operativi completi:

```text
metrica → query PromQL → condizione → stato alert → notifica webhook → runbook
```

La versione `v6.0` corregge il percorso GUI di Grafana 11.3, introduce un webhook locale verificabile, rende persistenti i dati principali mediante volumi Docker e distingue chiaramente arresto, riavvio e reset distruttivo.

## Sequenza consigliata

1. `00_OBS_UD21_Concetti_Alerting_Webhook_Persistenza_v6_0.md`
2. `07_OBS_UD21_GUIDA_ARCHITETTURA_Alerting_Webhook_Volumi_v6_0.md`
3. `06_OBS_UD21_APPROFONDIMENTO_Volumi_Persistenza_Docker_v6_0.md`
4. `08_OBS_UD21_APPROFONDIMENTO_Webhook_Payload_Routing_v6_0.md`
5. `04_OBS_UD21_GUIDA_OPERATIVA_Alerting_Webhook_Runbook_v6_0.md`
6. `01_OBS_UD21_LAB_guidato_Alerting_Webhook_Grafana_v6_0.md`
7. `02_OBS_UD21_MINI_ATTIVITA_Soglia_Alert_Runbook_v6_0.md`
8. `03_OBS_UD21_LAB_autonomo_Alert_Latenza_Webhook_v6_0.md`
9. `05_OBS_UD21_Raccordo_Alerting_Jaeger_Log_v6_0.md`

## Output atteso

Alla fine della UD il partecipante deve poter mostrare:

- stack locale avviato e servizi raggiungibili;
- volumi `grafana-data`, `prometheus-data` e `webhook-data` montati;
- contact point webhook testato con esito positivo;
- regola Grafana composta da query `A` e soglia `B`;
- folder, evaluation group e pending period configurati;
- passaggio `Normal → Pending → Alerting/Firing`;
- ricezione dei payload `firing` e `resolved` nel webhook receiver;
- runbook minimo collegato a metriche, log e trace;
- prova che `docker compose down` non cancella regole, contact point e dati persistenti.

## Avvio rapido

```bash
cd UD21/src/app_products_alerting
./scripts/start_stack_ud21.sh
./scripts/generate_traffic_ud21.sh
```

URL principali:

```text
Frontend:          http://localhost:8121
Prometheus:        http://localhost:9090
Grafana:           http://localhost:3000
Webhook receiver:  http://localhost:5001/events
Jaeger:            http://localhost:16686
```

Credenziali Grafana:

```text
admin / admin
```

## Arresto e reset: non sono la stessa cosa

Arresto normale, con volumi conservati:

```bash
./scripts/stop_stack_ud21.sh
```

Reset completo e distruttivo, da usare solo quando si vuole ricominciare da zero:

```bash
RESET_UD21=yes ./scripts/reset_stack_ud21.sh
```

Il reset elimina anche regole, contact point, cronologia Prometheus ed eventi webhook salvati nei volumi.
