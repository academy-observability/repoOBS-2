# UD28 — Dizionario dati

## File operativi

### `baseline_products_requests.csv`

60 osservazioni `base-*` raccolte tra 08:00 e 09:58 e usate per costruire il riferimento statistico. La baseline è volutamente più numerosa del set di evaluation.

### `evaluation_products_requests.csv`

20 osservazioni `eval-*` raccolte tra 10:00 e 10:38 e sottoposte al detector.

Colonne comuni:

| Colonna | Significato |
|---|---|
| observation_id | identificatore univoco dell'osservazione |
| timestamp_utc | istante dell'osservazione |
| environment | ambiente |
| service | servizio |
| endpoint | endpoint |
| status_code | status HTTP |
| duration_ms | durata in millisecondi |
| request_id | identificatore della richiesta |
| trace_id | identificatore del trace |

## Reference file

### `products_reference_labels.csv`

Contiene 20 informazioni di validazione riferite alle **stesse 20 `eval-*`** del file evaluation: una label per ogni osservazione.

| Colonna | Significato |
|---|---|
| observation_id | collega la label all'osservazione evaluation |
| reference_label | `normal` o `anomaly` secondo il processo di validazione |
| reference_reason_code | codice sintetico del motivo |
| reference_reason | spiegazione leggibile del motivo della label |
| label_source | processo da cui deriva la validazione |

Valori di `label_source` usati:

```text
service_review
controlled_test
incident_review
```

`reference_reason` non deve essere interpretato automaticamente come root cause.
