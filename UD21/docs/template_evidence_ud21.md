# Evidence UD21 — Alerting Grafana, webhook e persistenza

## Dati partecipante

- Nome:
- Data:
- Repository/cartella:

## Servizi

| Servizio | URL | Esito |
|---|---|---|
| Frontend | `http://localhost:8121` | |
| Prometheus | `http://localhost:9090` | |
| Grafana | `http://localhost:3000` | |
| Webhook receiver | `http://localhost:5001/events` | |
| Jaeger | `http://localhost:16686` | |

## Volumi

| Volume | Mount point | Verificato | Dato conservato |
|---|---|---|---|
| `obs-ud21-grafana-data` | `/var/lib/grafana` | | |
| `obs-ud21-prometheus-data` | `/prometheus` | | |
| `obs-ud21-webhook-data` | `/data` | | |

## Contact point

| Campo | Valore |
|---|---|
| Nome | |
| Tipo | |
| URL interna | |
| Test riuscito | |
| Evidenza nel receiver | |

## Alert error rate

| Campo | Valore |
|---|---|
| Rule name | |
| Query A | |
| Type A | |
| Expression B | |
| Alert condition | |
| Folder | |
| Evaluation group | |
| Evaluation interval | |
| Pending period | |
| Labels | |
| Contact point | |

## Stati e notifiche

| Evidenza | Risultato |
|---|---|
| Baseline Normal | |
| Pending | |
| Alerting/Firing | |
| Webhook firing | |
| Rientro Normal | |
| Webhook resolved | |

## Diagnosi

- Query di scomposizione:
- Log frontend:
- Log backend:
- Trace Jaeger:
- Causa osservata:
- Conclusione:

## Prova di persistenza

- Eseguito `stop_stack_ud21.sh`:
- Eseguito nuovo `start_stack_ud21.sh`:
- Regola ancora presente:
- Contact point ancora presente:
- Eventi webhook ancora presenti:
- Cronologia Prometheus ancora presente:

## Riflessione

- Perché la query osserva il frontend:
- Perché A è `Instant`:
- Perché B è la alert condition:
- Perché `down -v` è distruttivo:
- Che cosa non è persistente nello stack:
