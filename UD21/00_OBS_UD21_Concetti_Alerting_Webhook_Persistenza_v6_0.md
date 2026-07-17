# OBS UD21 — Concetti
# Alerting locale, webhook, persistenza e runbook sul Catalogo prodotti

## 0. Perché questa UD viene dopo metriche e dashboard

Un alert non è un grafico con un valore alto. È una decisione operativa codificata:

> quando un segnale supera una soglia, per un tempo sufficiente, il sistema deve cambiare stato e avvisare una destinazione identificata.

Per arrivare a questo risultato servono più passaggi distinti:

```text
Applicazione
   ↓ espone metriche
Prometheus
   ↓ esegue e conserva serie temporali
Grafana query A
   ↓ produce un valore
Espressione B Threshold
   ↓ confronta il valore con una soglia
Alert rule
   ↓ valuta ogni N secondi e applica il pending period
Contact point
   ↓ invia una notifica
Webhook receiver
   ↓ conserva e mostra il payload JSON
Runbook
   ↓ guida la diagnosi
```

Nelle UD precedenti abbiamo costruito i primi tre livelli. Qui completiamo il ciclo.

---

## 1. Lo scenario applicativo

Il servizio osservato è il Catalogo prodotti:

```text
Utente o script
      ↓
Frontend products :8121
      ↓ BACKEND_URL
Backend products :8021
```

Endpoint principali:

| Endpoint frontend | Comportamento |
|---|---|
| `/products` | richiesta normale |
| `/products/error` | errore 500 controllato |
| `/products/slow` | risposta lenta controllata |
| `/ready` | verifica della dipendenza frontend → backend |

L'applicazione produce:

- metriche Prometheus;
- log JSON su standard output;
- trace OpenTelemetry inviate a Jaeger.

Questa combinazione permette di distinguere il **segnale di allarme** dalla successiva **diagnosi**.

---

## 2. Query, condizione e alert non sono sinonimi

Nel laboratorio useremo due oggetti nella sezione Grafana **Define query and alert condition**.

### Query A

La query PromQL calcola l'error rate user-facing del frontend:

```promql
(
  sum(
    rate(
      app_http_requests_total{
        service="products-frontend",
        path=~"/products.*",
        status=~"5.."
      }[2m]
    )
  ) or vector(0)
)
/
clamp_min(
  sum(
    rate(
      app_http_requests_total{
        service="products-frontend",
        path=~"/products.*"
      }[2m]
    )
  ) or vector(0),
  0.001
)
```

Il risultato è un rapporto:

```text
0.00 = 0%
0.20 = 20%
0.50 = 50%
1.00 = 100%
```

La regola osserva intenzionalmente il frontend. In questo modo misura ciò che vede l'utente ed evita di contare due volte la stessa richiesta frontend → backend. Le metriche backend restano fondamentali per la diagnosi.


## Calcolo del tasso di errori HTTP 5xx

La query calcola la quota di richieste HTTP che hanno restituito un errore `5xx` sul servizio `products-frontend`, limitatamente ai path che iniziano con `/products`, negli ultimi 2 minuti.


La struttura logica è:

```text
tasso delle richieste con errore 5xx
───────────────────────────────────
tasso totale delle richieste
```

### 1. Selezione delle richieste con errore

Nel numeratore vengono considerate solo le richieste:

* del servizio `products-frontend`;
* dirette a path che iniziano con `/products`;
* con codice HTTP appartenente alla famiglia `5xx`.

```promql
status=~"5.."
```

La regular expression `5..` corrisponde, ad esempio, a `500`, `502`, `503` e `504`.

### 2. Calcolo del rate

```promql
rate(app_http_requests_total[2m])
```

`app_http_requests_total` è un contatore crescente.

La funzione `rate()` calcola la velocità media di incremento del contatore negli ultimi 2 minuti, espressa in richieste al secondo.

### 3. Somma delle serie

```promql
sum(...)
```

`sum()` aggrega tutte le serie corrispondenti, ad esempio quelle separate per istanza, path o codice HTTP, producendo un unico valore complessivo.

### 4. Gestione dell'assenza di dati

```promql
or vector(0)
```

Quando non esistono serie corrispondenti, Prometheus può restituire un risultato vuoto.

`or vector(0)` permette di utilizzare il valore `0` al posto di un vettore vuoto.

### 5. Calcolo del traffico totale

Il denominatore usa gli stessi filtri, ma non limita lo status HTTP:

```promql
app_http_requests_total{
  service="products-frontend",
  path=~"/products.*"
}
```

Vengono quindi considerate tutte le richieste, sia riuscite sia fallite.

### 6. Protezione dalla divisione per zero

```promql
clamp_min(..., 0.001)
```

`clamp_min()` impone al denominatore un valore minimo di `0.001`.

In questo modo, in assenza di traffico, viene evitata una divisione per zero.

### Interpretazione del risultato

La query restituisce un rapporto normalmente compreso tra `0` e `1`.

| Risultato | Percentuale di errori |
| --------: | --------------------: |
|       `0` |                    0% |
|    `0.01` |                    1% |
|    `0.05` |                    5% |
|    `0.20` |                   20% |
|       `1` |                  100% |

Ad esempio, un risultato pari a:

```text
0.05
```

significa che il 5% delle richieste ha restituito un errore HTTP `5xx`.

In Grafana è possibile visualizzare direttamente il valore come percentuale impostando l'unità del pannello su:

```text
Percent (0.0-1.0)
```

La query risponde quindi alla domanda:

> Negli ultimi 2 minuti, quale percentuale delle richieste ai path `/products...` del frontend ha generato un errore HTTP `5xx`?






### Espressione B — Threshold

La query A non contiene ancora la decisione. L'espressione B applica la soglia:

```text
Input A
IS ABOVE 0.20
```

B diventa la vera **Alert condition**.

```text
A = 0.12 → B = 0 → condizione falsa
A = 0.35 → B = 1 → condizione vera
```

---

## 3. Perché la query è di tipo Instant

Grafana può eseguire query `Range` o `Instant`.

- `Range` restituisce una sequenza di valori nel tempo;
- `Instant` restituisce il valore calcolato nell'istante di valutazione.

Nel laboratorio scegliamo `Instant`, perché la PromQL aggrega già tutte le serie in un solo valore. In questo caso possiamo collegare direttamente:

```text
Query A Instant → Threshold B
```

Se A fosse una query `Range`, dovremmo normalmente aggiungere una trasformazione `Reduce`, per esempio:

```text
Query A Range → Reduce last/mean/max → Threshold
```

Questa distinzione evita uno degli errori più frequenti nella GUI di Grafana.

---

## 4. Perché la query evita `NaN`

La forma più semplice dell'error rate è:

```promql
errori / richieste_totali
```

Quando non esiste ancora traffico, il calcolo può diventare:

```text
0 / 0 → NaN
```

`NaN` significa *Not a Number*: Grafana non dispone di un numero confrontabile con la soglia.

La query della UD usa due accorgimenti:

```promql
... or vector(0)
```

fornisce uno zero quando non esiste ancora una serie 5xx; mentre:

```promql
clamp_min(denominatore, 0.001)
```

impedisce che il denominatore sia zero.

Questa correzione evita un problema matematico dovuto all'assenza di traffico. Non nasconde invece un guasto reale di Prometheus: se il datasource non è raggiungibile, Grafana continua a segnalare un errore di valutazione.

---

## 5. Folder, evaluation group e pending period

Una alert rule Grafana-managed richiede elementi che nella precedente versione della UD non erano spiegati abbastanza.

### Folder

Il folder organizza le regole. Nel laboratorio creiamo:

```text
UD21
```

Non modifica il comportamento tecnico dell'alert, ma rende gestibile l'ambiente.

### Evaluation group

L'evaluation group stabilisce ogni quanto Grafana valuta le regole contenute nel gruppo:

```text
Nome: ud21-every-30s
Evaluation interval: 30s
```

### Pending period

Il pending period richiede che la condizione resti vera per un tempo minimo:

```text
Pending period: 1m
```

Sequenza:

```text
condizione falsa
   ↓
Normal

condizione vera alla prima valutazione
   ↓
Pending

condizione ancora vera per 1 minuto
   ↓
Alerting
```

Nell'elenco delle regole Grafana può mostrare lo stato aggregato `Firing`; l'istanza sottostante è nello stato `Alerting`. Nel linguaggio operativo vengono spesso usati entrambi i termini.

---

## 6. Contact point e notification policy

Un alert può cambiare stato senza notificare nessuno. Per inviare un messaggio serve una destinazione.

| Oggetto | Domanda a cui risponde |
|---|---|
| Contact point | Dove invio la notifica? |
| Notification policy | Quali alert vanno a quale contact point, con quali regole di routing e raggruppamento? |

Nella UD usiamo il percorso più leggibile per principianti:

```text
Alert rule → Select contact point → UD21 - Webhook locale
```

Le notification policy vengono spiegate, ma non sono obbligatorie nel laboratorio guidato. In ambienti reali sono preferibili quando esistono più team, severità e canali.

---

## 7. Perché il webhook è il contact point principale

L'email richiede un server SMTP, credenziali, TLS e configurazioni dipendenti dal provider. Questi aspetti sono reali, ma spostano l'attenzione dal ciclo di alerting.

Il webhook locale permette invece di osservare direttamente:

```text
HTTP POST
Content-Type: application/json
status: firing oppure resolved
labels
annotations
valori della regola
```

Il receiver della UD espone:

| Endpoint | Scopo |
|---|---|
| `POST /grafana-alert` | riceve la notifica da Grafana |
| `GET /events` | mostra gli eventi nel browser |
| `GET /api/events` | restituisce gli eventi in JSON |
| `GET /health` | verifica il servizio |
| `POST /clear` | cancella la cronologia del receiver |

La URL usata da Grafana è:

```text
http://webhook-receiver:5001/grafana-alert
```

Dal browser usiamo invece:

```text
http://localhost:5001/events
```

La differenza dipende dal punto da cui parte la connessione: dentro la rete Docker si usa il nome del servizio; dal computer host si usa la porta pubblicata su `localhost`.

---

## 8. Persistenza: perché i volumi fanno parte dell'architettura

Senza volumi, ricreare un container può eliminare dati importanti. La UD monta tre named volume:

| Volume | Mount point | Dati conservati |
|---|---|---|
| `obs-ud21-grafana-data` | `/var/lib/grafana` | database SQLite, utenti, regole, contact point, preferenze |
| `obs-ud21-prometheus-data` | `/prometheus` | TSDB e cronologia delle metriche |
| `obs-ud21-webhook-data` | `/data` | eventi JSON ricevuti dal webhook |

Questo permette di eseguire:

```bash
docker compose down
docker compose up -d
```

senza perdere il lavoro creato nella GUI.

Il comando seguente è invece distruttivo:

```bash
docker compose down -v
```

Per evitare cancellazioni involontarie, la UD separa due script:

```text
stop_stack_ud21.sh  → ferma i container e conserva i volumi
reset_stack_ud21.sh → elimina container e volumi, solo con conferma esplicita
```

Jaeger rimane volutamente con storage in memoria: in questa UD serve come supporto diagnostico immediato, non come archivio permanente delle trace. La differenza viene evidenziata per non creare l'idea errata che tutti i dati dello stack abbiano la stessa persistenza.

---

## 9. Stati `No Data` ed `Error`

`Normal`, `Pending` e `Alerting` descrivono il risultato della condizione. Esistono anche stati di salute della valutazione:

| Stato | Interpretazione |
|---|---|
| `No Data` | la query non ha prodotto serie utili |
| `Error` | query o datasource hanno generato un errore |

Non vanno confusi con `Normal`.

Esempi:

```text
Normal  → il sistema ha un valore valido e la soglia non è superata
No Data → il sistema non dispone di un valore valutabile
Error   → la valutazione non è riuscita
```

La query robusta riduce i casi di `No Data` dovuti al solo traffico assente, ma un target `DOWN` o un datasource irraggiungibile resta un problema operativo da investigare.

---

## 10. Firing e resolved

Il ciclo non termina quando parte l'allarme.

```text
Normal → Pending → Alerting/Firing → Normal
```

Il webhook riceve normalmente:

```json
{"status": "firing"}
```

quando il problema è attivo e:

```json
{"status": "resolved"}
```

quando la condizione rientra.

Un sistema di alerting utile deve comunicare sia l'apertura sia la risoluzione, altrimenti l'operatore non sa se il problema è ancora presente.

---

## 11. Runbook: dall'allarme alla diagnosi

Un alert descrive un sintomo, non necessariamente la causa.

```text
Alert error rate
      ↓
Dashboard: quanto e dove?
      ↓
PromQL: quale serie contribuisce?
      ↓
Log: quale request_id e quale errore?
      ↓
Jaeger: dove si trova il tempo o il fallimento?
      ↓
Conclusione e azione
```

Per questo ogni regola deve avere almeno:

- summary comprensibile;
- description operativa;
- label `service`, `severity`, `ud`;
- riferimento al runbook;
- prima verifica concreta.

---

## 12. Risultato formativo

Al termine della UD il partecipante deve saper spiegare:

> La query A calcola un indicatore numerico. L'espressione B applica la soglia ed è la vera alert condition. Grafana valuta la regola nell'evaluation group, applica il pending period e, quando lo stato diventa Alerting, invia un payload JSON al contact point webhook. I dati di Grafana, Prometheus e del receiver restano disponibili perché sono conservati in volumi Docker. Il runbook guida poi l'analisi con metriche, log e trace.
