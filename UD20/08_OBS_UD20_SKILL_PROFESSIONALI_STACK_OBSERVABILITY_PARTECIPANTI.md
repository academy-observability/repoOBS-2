# OBS UD20 — Competenze professionali per gestire uno stack di Observability

## 0. Una premessa importante

Quando osserviamo uno stack composto da strumenti come:

- Docker;
- Prometheus;
- Grafana;
- Jaeger;
- OpenTelemetry;
- applicazioni frontend e backend;

può sembrare che sia necessario conoscere tutto in modo approfondito fin dal primo giorno.

In realtà, nel lavoro le competenze si costruiscono progressivamente.

Nessuno inizia sapendo configurare contemporaneamente applicazioni, rete, metriche, dashboard, tracing, alerting, sicurezza e automazione. Anche nei team professionali le responsabilità sono spesso distribuite tra più ruoli:

- sviluppatori;
- sistemisti;
- DevOps Engineer;
- Cloud Engineer;
- Platform Engineer;
- Site Reliability Engineer;
- Observability Engineer.

L'obiettivo iniziale non è diventare immediatamente esperti di ogni componente.

L'obiettivo realistico è imparare a:

1. comprendere come comunicano i componenti;
2. seguire il percorso dei dati osservabili;
3. riconoscere dove può trovarsi un problema;
4. applicare una sequenza ordinata di verifiche;
5. documentare ciò che è stato osservato.

Queste sono già competenze professionali concrete.

---

# 1. Che cosa significa “gestire uno stack di Observability”

Gestire uno stack di Observability significa assicurarsi che:

- le applicazioni producano dati osservabili;
- Prometheus raccolga correttamente le metriche;
- Grafana riesca a interrogarle e visualizzarle;
- Jaeger riceva e mostri le trace;
- i log siano leggibili e correlabili;
- dashboard e alert rispondano a domande operative reali;
- configurazioni e dati siano mantenuti in modo affidabile.

Non significa conoscere a memoria ogni opzione di ogni strumento.

Significa soprattutto saper ragionare sulla catena:

```text
Applicazione
    ↓
Telemetria
    ↓
Raccolta
    ↓
Archiviazione
    ↓
Query
    ↓
Dashboard e alert
    ↓
Decisione operativa
```

---

# 2. Le competenze non si acquisiscono tutte insieme

Possiamo suddividerle in tre livelli.

## Livello 1 — Competenze da acquisire durante il percorso

Sono le competenze essenziali per iniziare a lavorare in modo guidato:

- capire la differenza tra metriche, log e trace;
- usare Docker Compose;
- controllare lo stato dei container;
- leggere i log di un container;
- verificare un endpoint `/health`;
- verificare un endpoint `/metrics`;
- controllare i target Prometheus;
- eseguire query PromQL semplici;
- leggere una dashboard Grafana;
- individuare un servizio lento o in errore;
- documentare le evidenze.

Queste attività sono già presenti nei laboratori.

---

## Livello 2 — Competenze che si consolidano con la pratica

Dopo avere acquisito le basi, si impara progressivamente a:

- progettare dashboard;
- modificare query PromQL;
- configurare datasource;
- gestire dashboard tramite provisioning;
- creare alert;
- leggere trace distribuite;
- correlare metriche, log e trace;
- riconoscere problemi di rete Docker;
- gestire volumi e persistenza;
- ridurre il rumore degli alert;
- interpretare latenza, errori e saturazione.

Non è necessario padroneggiare tutto immediatamente.

---

## Livello 3 — Competenze avanzate

Le competenze avanzate arrivano normalmente con esperienza su sistemi reali:

- Kubernetes;
- alta disponibilità;
- gestione di grandi volumi di metriche;
- controllo della cardinalità;
- retention;
- sicurezza;
- multi-tenancy;
- SLI e SLO;
- error budget;
- automazione completa;
- Infrastructure as Code;
- gestione strutturata degli incidenti;
- ottimizzazione dei costi.

Questi argomenti non rappresentano il punto di partenza.

Sono un'evoluzione naturale delle competenze di base.

---

# 3. Le aree principali

## 3.1 Sistemi operativi e troubleshooting

È utile saper usare alcuni comandi Linux:

```bash
ps
top
free -m
df -h
ss -lntp
curl
systemctl
journalctl
```

In ambiente Docker:

```bash
docker compose ps
docker logs
docker inspect
docker stats
docker exec
```

Non è necessario memorizzarli tutti.

È più importante sapere quale domanda ci aiutano a risolvere.

| Domanda | Comando possibile |
|---|---|
| Il container è attivo? | `docker compose ps` |
| L'applicazione ha prodotto errori? | `docker logs` |
| Quali porte sono pubblicate? | `docker inspect` |
| Il servizio risponde? | `curl` |
| CPU o memoria sono elevate? | `docker stats` |

---

## 3.2 Docker e reti

Per il nostro stack è utile comprendere:

- immagini;
- container;
- porte;
- volumi;
- reti;
- variabili d'ambiente;
- nomi dei servizi Docker.

Un concetto importante è la differenza tra:

```text
localhost
```

e:

```text
nome-servizio
```

Dal browser possiamo raggiungere Prometheus con:

```text
http://localhost:9090
```

Grafana, invece, dal proprio container raggiunge Prometheus con:

```text
http://prometheus:9090
```

Non è un dettaglio da imparare a memoria: è una conseguenza del funzionamento delle reti Docker.

---

## 3.3 Metriche e Prometheus

Le metriche principali sono:

### Counter

Un valore cumulativo che cresce.

Esempio:

```text
app_http_requests_total
```

Viene usato per contare:

- richieste;
- errori;
- eventi;
- operazioni completate.

Query tipica:

```promql
rate(app_http_requests_total[5m])
```

---

### Gauge

Un valore che può aumentare e diminuire.

Esempi:

```text
active_connections
queue_size
memory_usage
```

---

### Histogram

Raccoglie una distribuzione di valori, per esempio la durata delle richieste.

Esempi:

```text
app_http_request_duration_seconds_bucket
app_http_request_duration_seconds_sum
app_http_request_duration_seconds_count
```

Permette di calcolare percentili come il p95.

Non è necessario conoscere subito tutte le formule.

È sufficiente comprendere il significato operativo:

> Il p95 indica entro quale durata termina approssimativamente il 95% delle richieste.

---

## 3.4 Grafana

Grafana serve a trasformare metriche e query in informazioni leggibili.

Ogni pannello dovrebbe rispondere a una domanda.

| Pannello | Domanda |
|---|---|
| Target UP | Prometheus riesce a raggiungere il servizio? |
| Request rate | Quanto traffico sta ricevendo? |
| Error rate | Quanti errori vengono prodotti? |
| Latenza p95 | Quanto attendono le richieste più lente? |
| Richieste totali | Quante richieste sono state elaborate? |

Il valore di una dashboard non dipende dal numero di grafici.

Dipende dalla capacità di supportare una decisione.

---

## 3.5 Log

I log aiutano a comprendere gli eventi.

Un log utile contiene informazioni come:

```json
{
  "timestamp": "2026-07-15T10:30:00Z",
  "level": "ERROR",
  "service": "products-backend",
  "path": "/api/products",
  "status": 500,
  "request_id": "abc-123"
}
```

Nel lavoro è utile riconoscere:

- timestamp;
- livello;
- servizio;
- endpoint;
- codice HTTP;
- identificatore della richiesta;
- messaggio di errore.

Non è indispensabile diventare subito esperti di tutte le piattaforme di log.

La capacità fondamentale è saper cercare l'evidenza utile.

---

## 3.6 Trace e OpenTelemetry

Una trace segue una richiesta attraverso più componenti.

Esempio:

```text
Utente
  ↓
Frontend
  ↓
Backend
  ↓
Database
```

La trace permette di capire:

- quanto tempo è stato trascorso nel frontend;
- quanto tempo è stato trascorso nel backend;
- quale chiamata è risultata lenta;
- dove si è verificato un errore;
- quale dipendenza ha causato il ritardo.

Nel nostro percorso Jaeger e OpenTelemetry servono soprattutto a introdurre questo modello mentale.

---

# 4. La competenza più importante: seguire una catena diagnostica

Nel lavoro non è necessario conoscere immediatamente la risposta.

È molto più importante saper procedere in modo ordinato.

Esempio:

```text
Grafana mostra “No data”
```

La sequenza di verifica può essere:

```text
1. Il container dell'applicazione è attivo?
2. L'applicazione risponde su /health?
3. Espone /metrics?
4. Prometheus vede il target come UP?
5. La metrica è presente?
6. La query restituisce dati?
7. Grafana usa il datasource corretto?
8. Il time range è corretto?
```

Comandi possibili:

```bash
docker compose ps
docker logs ud20-products-backend
curl http://localhost:8020/health
curl http://localhost:8020/metrics
```

Query Prometheus:

```promql
up{job="products-backend"}
```

e:

```promql
app_http_requests_total{
  service="products-backend"
}
```

Questo metodo è trasferibile anche ad altri stack.

---

# 5. PromQL: quanto bisogna saperne all'inizio

Per iniziare è sufficiente conoscere alcune funzioni:

```promql
sum()
avg()
max()
min()
rate()
increase()
histogram_quantile()
```

e alcuni operatori:

```promql
by (...)
=~
!~
```

Esempio:

```promql
sum by (service, path, status) (
  rate(app_http_requests_total[5m])
)
```

Non è necessario scrivere subito query complesse senza supporto.

Nel lavoro è normale:

- partire da query già esistenti;
- modificarle;
- provarle in Prometheus;
- confrontare il risultato;
- consultare documentazione;
- sottoporle a revisione.

---

# 6. Alerting

Gli alert servono a richiamare l'attenzione quando una condizione richiede intervento.

Un alert troppo semplice:

```text
CPU superiore al 50%
```

può produrre rumore.

Un alert più significativo potrebbe essere:

```text
CPU superiore all'85% per 10 minuti
e latenza p95 superiore a 2 secondi
```

Con l'esperienza si impara a:

- scegliere soglie;
- impostare una durata;
- evitare falsi positivi;
- collegare l'alert a una dashboard;
- indicare un possibile runbook.

Nel livello iniziale è sufficiente comprendere il principio:

> Un alert utile deve essere collegato a un possibile impatto e a una possibile azione.

---

# 7. Automazione e configurazione come codice

Molte configurazioni dello stack possono essere versionate:

```text
prometheus.yml
dashboard JSON
datasource YAML
alert rules
docker-compose.yml
OpenTelemetry configuration
```

Questo approccio permette:

- ripetibilità;
- condivisione;
- controllo delle versioni;
- rollback;
- revisione;
- distribuzione coerente.

Nel nostro laboratorio la dashboard provisionata è già un esempio di configurazione come codice.

---

# 8. Sicurezza

Le piattaforme di Observability possono contenere informazioni sensibili.

È importante evitare di inserire nei log o nelle metriche:

- password;
- token;
- connection string;
- dati personali non necessari;
- segreti applicativi.

Le competenze avanzate comprendono anche:

- autenticazione;
- autorizzazione;
- TLS;
- gestione dei secret;
- retention;
- auditing.

Anche in questo caso non è necessario affrontare tutto contemporaneamente.

Il primo passo è sviluppare attenzione verso ciò che viene raccolto.

---

# 9. Quali ruoli lavorano con queste competenze

Lo stack di Observability può essere gestito da ruoli differenti.

## Junior Monitoring o Observability Operator

Attività tipiche:

- controllare dashboard;
- verificare alert;
- controllare target e container;
- raccogliere evidenze;
- eseguire troubleshooting guidato;
- aprire o aggiornare ticket;
- seguire runbook.

---

## DevOps o Cloud Engineer

Attività tipiche:

- gestire deployment;
- configurare metriche e log;
- integrare lo stack con pipeline;
- amministrare container e infrastruttura;
- automatizzare configurazioni.

---

## Platform o Observability Engineer

Attività tipiche:

- progettare la piattaforma;
- definire standard;
- gestire provisioning;
- controllare prestazioni e costi;
- integrare metriche, log e trace;
- supportare più team.

---

## Site Reliability Engineer

Attività tipiche:

- definire SLI e SLO;
- gestire error budget;
- migliorare affidabilità;
- ridurre alert inutili;
- guidare incident response;
- analizzare cause e azioni correttive.

Questi ruoli rappresentano possibili evoluzioni, non prerequisiti per iniziare.

---

# 10. Obiettivo realistico del percorso

Al termine del percorso un partecipante non deve necessariamente essere in grado di progettare da solo una piattaforma enterprise completa.

Un obiettivo realistico è diventare capace di:

- comprendere l'architettura dello stack;
- avviare e verificare i componenti;
- leggere metriche, log e trace;
- usare query già note;
- modificare semplici dashboard;
- riconoscere problemi comuni;
- seguire una procedura diagnostica;
- raccogliere evidenze;
- comunicare in modo tecnico ciò che è stato osservato.

Queste competenze sono una base concreta per ruoli junior.

---

# 11. Skill matrix iniziale

Per lo stack del percorso:

```text
Flask
Docker
Prometheus
Grafana
Jaeger
OpenTelemetry
```

la matrice iniziale può essere:

| Competenza | Obiettivo del percorso |
|---|---|
| Linux CLI | Utilizzo operativo di base |
| Bash | Lettura e piccole modifiche |
| Python/Flask | Comprensione del flusso applicativo |
| HTTP e API REST | Comprensione intermedia |
| Docker | Uso operativo |
| Docker Compose | Avvio, stop e diagnosi |
| Networking Docker | Concetti fondamentali |
| Prometheus | Target, metriche e query principali |
| PromQL | Query semplici e modifica di query esistenti |
| Grafana | Lettura e creazione di pannelli |
| OpenTelemetry | Concetti fondamentali |
| Jaeger | Lettura di trace |
| Git | Versionamento di base |
| YAML e JSON | Lettura e modifica controllata |
| Troubleshooting | Metodo strutturato |
| Documentazione | Raccolta e descrizione delle evidenze |

---

# 12. Come continuare dopo il corso

Un possibile percorso di crescita è:

```text
1. Consolidare Docker e networking
2. Esercitarsi con PromQL
3. Costruire piccole dashboard
4. Analizzare log strutturati
5. Leggere trace distribuite
6. Creare alert semplici
7. Versionare le configurazioni
8. Avvicinarsi a Kubernetes
9. Studiare SLI e SLO
10. Lavorare su casi reali
```

Non è necessario completare tutti questi passaggi in poco tempo.

La crescita avviene attraverso:

- ripetizione;
- casi pratici;
- errori controllati;
- troubleshooting;
- confronto con il team;
- documentazione.

---

# 13. Messaggio conclusivo

Gestire uno stack di Observability richiede diverse competenze, ma non è necessario possederle tutte fin dall'inizio.

Il primo traguardo professionale è più concreto:

> Saper osservare un sistema, raccogliere evidenze e seguire una procedura ordinata per capire dove si trova un problema.

Da questa base si sviluppano progressivamente:

- autonomia;
- capacità di progettazione;
- automazione;
- gestione degli alert;
- affidabilità;
- competenze cloud e SRE.

Il laboratorio non pretende di trasformare immediatamente il partecipante in uno specialista senior.

Serve invece a costruire il metodo, il linguaggio tecnico e le capacità operative da cui può iniziare una crescita professionale reale.
