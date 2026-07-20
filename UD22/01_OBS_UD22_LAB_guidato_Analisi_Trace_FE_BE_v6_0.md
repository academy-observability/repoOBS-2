# OBS UD22 — Laboratorio guidato
# Analisi di trace frontend–backend con Jaeger

## Obiettivo

Ricostruire tre richieste controllate — normale, lenta e in errore — e dimostrare, con trace e log, dove viene consumato il tempo e dove nasce l'errore.

## Task 1 — Preparazione

Prima di avviare la UD22 fermiamo gli stack locali che occupano le stesse porte. Dalla cartella di lavoro della UD21, se ancora attiva:

```bash
./scripts/stop_stack_ud21.sh
```

Entriamo quindi nella cartella:

```bash
cd UD22/src/app_products_tracing
chmod +x scripts/*.sh
./scripts/start_stack_ud22.sh
```

Apriamo:

```text
Frontend   http://localhost:8122
Jaeger     http://localhost:16686
Grafana    http://localhost:3000
```

### Osservazione sui volumi

Lo script segnala tre named volume. In questa UD ci interessa soprattutto:

```text
obs-ud22-jaeger-data -> /badger
```

Badger è il database usato da Jaeger; il volume conserva i suoi file anche quando il container viene ricreato.

## Task 2 — Generare gli scenari

```bash
./scripts/generate_trace_scenarios_ud22.sh
```

Lo script genera:

```text
normal  /products
slow    /products/slow
error   /products/error
```

Per ogni caso annotiamo:

- `request_id`;
- `trace_id`;
- URL diretto della trace.

Attendiamo alcuni secondi e apriamo il primo URL Jaeger.

## Task 3 — Trace normale

Nella trace normale individuiamo:

```text
GET /products
└── GET backend-products:8000/api/products
    └── GET /api/products
        └── catalog.load_products
```

La forma del nome HTTP può includere host o route, ma devono risultare riconoscibili:

- uno span SERVER del frontend;
- uno span CLIENT del frontend;
- uno span SERVER del backend;
- uno span INTERNAL del backend.

Compiliamo:

```text
Durata totale:
Numero di servizi:
Span più lungo:
Stato HTTP:
```

### Domanda

Perché client span e server span del backend si sovrappongono temporalmente invece di sommarsi uno dopo l'altro?

## Task 4 — Trace lenta

Apriamo la trace `slow`.

Confrontiamo:

- durata totale della trace;
- durata del client span frontend;
- durata del server span backend;
- durata di `catalog.load_products`.

Il dato atteso è una concentrazione del tempo nel backend. Scriviamo una conclusione completa:

```text
La richiesta è lenta perché...
L'evidenza principale è...
Il servizio coinvolto è...
```

Non usiamo formule generiche come “la rete è lenta” se la trace non lo dimostra.

## Task 5 — Trace in errore

Apriamo la trace `error`.

Verifichiamo:

- status HTTP `500`;
- span evidenziati come errore;
- servizio in cui compare `catalog.load_products.error`;
- attributo `error.type`;
- propagazione dell'esito verso il frontend.

Completiamo:

```text
Origine dell'errore:
Span che rappresenta l'operazione fallita:
Effetto osservato dal frontend:
```

## Task 6 — Correlazione con i log

Scegliamo il `request_id` della richiesta lenta:

```bash
./scripts/show_correlated_logs_ud22.sh REQUEST_ID
```

Confrontiamo le due righe JSON.

| Campo | Frontend | Backend |
|---|---|---|
| `request_id` | | |
| `trace_id` | | |
| `span_id` | | |
| `path` | | |
| `status` | | |
| `latency_ms` | | |

Dobbiamo osservare:

```text
stesso request_id
stesso trace_id
span_id differenti
path differenti ma causalmente collegati
```

## Task 7 — Dal segnale aggregato alla trace

Apriamo Grafana e la dashboard della UD22. Generiamo nuovamente due richieste lente e due errori:

```bash
curl -s http://localhost:8122/products/slow >/dev/null
curl -s http://localhost:8122/products/slow >/dev/null
curl -s http://localhost:8122/products/error >/dev/null
curl -s http://localhost:8122/products/error >/dev/null
```

Dopo lo scrape osserviamo latenza ed error rate. Spieghiamo la relazione:

```text
Grafana indica che esiste un sintomo aggregato.
Jaeger permette di analizzare una richiesta rappresentativa.
I log aggiungono i dettagli applicativi della stessa richiesta.
```

## Task 8 — Verifica guidata della persistenza

Generiamo una trace riconoscibile:

```bash
./scripts/generate_persistence_trace_ud22.sh
```

Apriamo l'URL stampato e annotiamo il `trace_id`. Poi ricreiamo i container:

```bash
./scripts/restart_stack_ud22.sh
```

Dopo il riavvio riapriamo:

```text
http://localhost:16686/trace/TRACE_ID
```

La trace deve essere ancora disponibile perché Badger scrive nel named volume `obs-ud22-jaeger-data`, montato in `/badger`.

Questa prova non significa che ogni trace venga conservata per sempre: persistenza e retention sono concetti distinti.

## Task 9 — Evidenza finale

Compiliamo `docs/template_evidence_ud22.md` indicando:

- trace normale;
- trace lenta;
- trace in errore;
- correlazione log;
- verifica della persistenza;
- diagnosi sintetica.
