# Dizionario dati — mini_products_requests.csv

| Colonna | Significato |
|---|---|
| `observation_id` | identificatore univoco della singola osservazione |
| `timestamp_utc` | momento dell'osservazione in UTC |
| `environment` | ambiente di esecuzione |
| `service` | servizio che ha prodotto l'osservazione |
| `endpoint` | endpoint HTTP osservato |
| `status_code` | status HTTP |
| `duration_ms` | durata dell'osservazione in millisecondi |
| `request_id` | identificatore della richiesta |
| `trace_id` | identificatore usato per correlare il percorso distribuito |

## Granularità

Una riga rappresenta una singola osservazione di richiesta per un servizio.

Due righe possono condividere `request_id` e `trace_id` quando la stessa richiesta attraversa frontend e backend.
