# OBS UD22 — Guida operativa
# Cercare trace e correlare le evidenze

## 1. Avvio

Dalla cartella `UD22/src/app_products_tracing`:

```bash
chmod +x scripts/*.sh
./scripts/start_stack_ud22.sh
```

Lo script verifica l'accessibilità dei servizi e riepiloga anche i tre volumi montati. Il volume centrale della UD è:

```text
obs-ud22-jaeger-data -> /badger
```

## 2. Interfaccia Jaeger

Apriamo:

```text
http://localhost:16686
```

Nella ricerca principale possiamo selezionare:

- Service;
- Operation;
- Tags;
- Lookback;
- durata minima o massima.

Dopo le prime richieste devono comparire i servizi:

```text
products-frontend
products-backend
```

Gli span vengono esportati in batch. Dopo una richiesta attendiamo alcuni secondi prima di concludere che una trace sia assente.

## 3. Apertura diretta tramite trace ID

Gli script estraggono il `trace_id` dalla risposta e mostrano un URL:

```text
http://localhost:16686/trace/TRACE_ID
```

Questo metodo è particolarmente utile perché elimina l'ambiguità temporale: apriamo esattamente la trace generata.

## 4. Lettura ordinata della trace

Seguiamo sempre la stessa sequenza:

1. verifichiamo il nome dell'operazione radice;
2. leggiamo la durata totale;
3. contiamo i servizi coinvolti;
4. espandiamo gli span;
5. individuiamo il ramo più lungo;
6. leggiamo gli attributi HTTP e applicativi;
7. controlliamo lo stato degli span;
8. formuliamo una conclusione.

Per una richiesta lenta non basta dire “vedo 2,5 secondi”. Dobbiamo dire:

> La durata è concentrata nello span `catalog.load_products` del servizio `products-backend`; il frontend trascorre la maggior parte del tempo in attesa della risposta del backend.

## 5. Correlazione con i log

Per cercare un `request_id` nei due servizi:

```bash
./scripts/show_correlated_logs_ud22.sh REQUEST_ID
```

Le righe JSON devono mostrare lo stesso:

```text
request_id
trace_id
```

Lo `span_id` è diverso perché il log frontend e quello backend appartengono a span SERVER diversi.

## 6. Metriche come punto di partenza

Grafana contiene la dashboard:

```text
UD22 - Metriche di contesto per l’analisi delle trace
```

La dashboard non sostituisce Jaeger. Serve a riconoscere un sintomo aggregato, per esempio:

- aumento dei 5xx;
- aumento del p95;
- servizio non raggiungibile.

Da quel punto selezioniamo una richiesta controllata e passiamo alla trace.

## 7. Salvataggio delle evidenze

Per conservare i log dei container:

```bash
./scripts/save_logs_ud22.sh
```

Le evidenze vengono salvate nella cartella `UD22/logs`. Le trace rimangono nel database Badger montato sul volume Jaeger finché non scade la retention o non viene eseguito un reset distruttivo.
