# Academy Observability
# Programma generale del percorso

## Presentazione iniziale per i partecipanti

Benvenuti nel percorso **Academy Observability**.

Questo documento presenta il programma generale del corso, l'organizzazione delle attività e gli obiettivi formativi principali.

Il programma è da considerarsi **un programma di massima**.  
Alcuni argomenti potranno essere approfonditi più di altri in base a:

- tempo effettivamente disponibile;
- livello di partenza del gruppo;
- ambienti tecnici utilizzabili;
- andamento dei laboratori;
- problemi tecnici emersi;
- priorità didattiche;
- obiettivi del project work finale.

Non tutti i punti indicati saranno necessariamente trattati con lo stesso livello di dettaglio.

La priorità sarà sempre data a:

- comprensione operativa;
- pratica di laboratorio;
- metodo di troubleshooting;
- produzione di evidenze;
- capacità di ragionare sui segnali tecnici.

---

## Durata e organizzazione generale

Il percorso ha una durata complessiva prevista di:

```text
216 ore
```

Le attività saranno organizzate in **sessioni da 4 ore**.

Di norma, una giornata completa sarà composta da due sessioni:

```text
4 ore al mattino
+ 4 ore al pomeriggio
= 8 ore
```

La prima giornata del percorso sarà una sessione iniziale da **4 ore**, dedicata all'avvio del corso, alla configurazione del repository personale e alla verifica dell'ambiente di lavoro.

L'organizzazione complessiva può essere letta così:

```text
54 sessioni da 4 ore
= 216 ore
```

Oppure, in forma equivalente:

```text
prima sessione di avvio da 4 ore
+ giornate complete da 8 ore
+ eventuale sessione conclusiva di chiusura
= 216 ore complessive
```

---

## Struttura didattica delle giornate

Nelle giornate complete da 8 ore useremo, quando possibile, questa organizzazione:

| Fase | Durata indicativa | Attività |
|---|---:|---|
| Sessione mattutina | 4h | Concetti, dimostrazione e laboratorio guidato |
| Sessione pomeridiana | 4h | Briefing docente, laboratorio autonomo, evidenze, report e commit |

La prima sessione da 4 ore sarà invece dedicata soprattutto a:

- presentazione del percorso;
- accesso a GitHub Classroom;
- creazione del repository personale;
- clone locale;
- primo commit;
- primo push;
- impostazione della struttura di lavoro.

---

## Metodo di lavoro

Il repository personale di ogni partecipante sarà usato come diario tecnico del corso.

Il flusso di lavoro sarà:

```text
attività pratica
→ file prodotti
→ evidenze
→ report
→ commit
→ push
```

Durante il corso non lavoreremo solo sul risultato finale, ma anche sul modo in cui il risultato viene costruito, verificato e documentato.

---

## Obiettivo generale del percorso

L'obiettivo del corso è sviluppare competenze operative e progettuali nell'ambito dell'**Observability** applicata a sistemi, applicazioni, infrastrutture cloud e processi DevOps.

L'Observability non significa solo guardare grafici.

Significa imparare a rispondere a domande come:

- il servizio è disponibile?
- cosa è cambiato?
- dove si concentra l'errore?
- quale componente è lento?
- il problema è recente o ricorrente?
- l'errore è collegato a una nuova release?
- quali evidenze supportano la diagnosi?
- quale azione correttiva è ragionevole?

---

## Che cosa intendiamo per Observability

Per Observability intendiamo la capacità di comprendere lo stato interno di un sistema osservando i segnali che esso produce.

I segnali principali sono:

| Segnale | Significato |
|---|---|
| Log | Eventi e messaggi prodotti da sistemi e applicazioni |
| Metriche | Valori numerici osservati nel tempo |
| Trace | Percorso di una richiesta attraverso più componenti |
| Eventi | Cambiamenti significativi nello stato del sistema |

Durante il percorso lavoreremo su questi segnali a livelli diversi:

```text
sistema operativo
→ rete
→ applicazione
→ container
→ cloud
→ pipeline
→ dashboard
→ incidente
→ project work
```

---

# Struttura di massima del percorso

Il percorso sarà organizzato in 6 moduli.

Le ore indicate sono orientative e potranno essere adattate in base all'andamento reale del corso.

| Modulo | Ore indicative | Sessioni da 4h | Focus |
|---|---:|---:|---|
| Modulo 1 | 40h | 10 | Fondamenta operative, Linux, rete e primo servizio osservabile |
| Modulo 2 | 44h | 11 | Azure, risorse cloud, Log Analytics, KQL, alert e dashboard |
| Modulo 3 | 52h | 13 | DevOps, CI/CD, container, release observability, tracing e OpenTelemetry |
| Modulo 4 | 44h | 11 | Prometheus, Grafana, log centralizzati, strumenti enterprise e RCA |
| Modulo 5 | 20h | 5 | ML/AI applicati a dati osservabili |
| Modulo 6 | 16h | 4 | Project work finale, revisione e presentazione |
| **Totale** | **216h** | **54** |  |

Questa distribuzione riduce il tempo dedicato al project work finale rispetto a una versione più estesa del programma, per lasciare più spazio ai moduli tecnici più importanti.

---

# Modulo 1
## Fondamenta operative, Linux, rete e primo servizio osservabile

### Durata indicativa

```text
40 ore
10 sessioni da 4 ore
```

### Obiettivo del modulo

Costruire le basi operative necessarie per lavorare con sistemi, terminale, file, processi, rete e primi segnali osservabili.

### Argomenti principali

- Presentazione del percorso.
- GitHub Classroom e repository personale.
- Git di base:
  - clone;
  - status;
  - add;
  - commit;
  - push.
- Struttura del repository di laboratorio.
- Setup ambiente di lavoro.
- Linux e shell.
- File system, path, directory e file.
- Redirection, pipe e comandi testuali.
- Permessi, utenti e gruppi.
- Processi e diagnostica locale.
- Porte, socket e servizi.
- Diagnostica di rete.
- HTTP, endpoint e codici di stato.
- Log applicativi.
- Log JSON.
- Request ID.
- Endpoint `/health` e `/ready`.
- Metriche semplici.
- SLI di base.
- Primo servizio osservabile locale.

### Competenze attese

Al termine del modulo dovremmo essere in grado di:

- usare un repository Git per salvare il lavoro;
- muoverci in un ambiente Linux di base;
- leggere e produrre file di evidenza;
- eseguire comandi diagnostici;
- riconoscere problemi su processi, porte e servizi;
- interrogare endpoint HTTP;
- leggere log semplici;
- comprendere il valore di health check, readiness e metriche minime;
- produrre un primo report tecnico.

---

# Modulo 2
## Azure, risorse cloud, Log Analytics, KQL, alert e dashboard

### Durata indicativa

```text
44 ore
11 sessioni da 4 ore
```

### Obiettivo del modulo

Portare il ragionamento sull'Observability in ambiente cloud, con particolare attenzione a Microsoft Azure.

### Argomenti principali

- Tenant, subscription e Resource Group.
- Naming convention e tag.
- Governance minima delle risorse.
- Cost control.
- Activity Log.
- Risorse Azure fondamentali, in base agli ambienti disponibili:
  - Storage Account;
  - VM Linux;
  - App Service;
  - container runtime;
  - Azure SQL o persistenza dati.
- Stato e diagnostica delle risorse.
- Azure Monitor.
- Metriche di piattaforma.
- Aggregazioni e dimensioni.
- Diagnostic settings.
- Log Analytics Workspace.
- Tabelle e schema.
- KQL di base.
- Filtri, proiezioni e ordinamenti.
- Aggregazioni con `summarize`.
- Trend temporali con `bin()`.
- Analisi errori.
- Error rate.
- Percentili e latenze.
- Query candidate per alert.
- Alert rule.
- Action group.
- Dashboard e workbook.
- Revisione architettura e cleanup.

### Competenze attese

Al termine del modulo dovremmo essere in grado di:

- creare e documentare risorse Azure minime;
- riconoscere i principali segnali di piattaforma;
- distinguere Activity Log, metriche e resource logs;
- usare Azure Monitor per analizzare metriche;
- comprendere il ruolo dei diagnostic settings;
- interrogare dati con KQL;
- costruire query di troubleshooting;
- progettare un alert utile;
- distinguere un alert utile da un alert rumoroso;
- progettare una dashboard o un workbook operativo.

---

# Modulo 3
## DevOps, CI/CD, container, release observability, tracing e OpenTelemetry

### Durata indicativa

```text
52 ore
13 sessioni da 4 ore
```

### Obiettivo del modulo

Collegare l'Observability al ciclo di sviluppo e rilascio del software.

Un problema in produzione spesso non nasce solo nel runtime. Può nascere da una modifica, da una build, da una pipeline, da una configurazione o da un deploy.

### Argomenti principali

- Repository come fonte di verità tecnica.
- Commit, branch e tracciabilità delle modifiche.
- Pull request e revisione.
- Continuous Integration.
- Quality gate.
- Test automatici.
- Workflow GitHub Actions.
- Azure Pipelines.
- Artifact.
- Manifest di release.
- Ambienti:
  - local;
  - dev;
  - test;
  - staging;
  - production.
- Variabili e segreti.
- Packaging applicativo.
- Dockerfile.
- Build container.
- Immagini container.
- Registry e tag immagine.
- Container locale.
- Health check containerizzati.
- Log runtime.
- Variabili runtime.
- Pipeline multi-stage.
- Deploy controllato.
- Smoke test.
- Rollback.
- Release-aware logging.
- Build ID.
- Versione applicativa.
- Correlation ID.
- OpenTelemetry.
- Trace e span.
- Context propagation.
- Introduzione al tracing.
- Incident response su pipeline.
- Runbook operativo.

### Competenze attese

Al termine del modulo dovremmo essere in grado di:

- comprendere il ruolo del repository nel ciclo DevOps;
- leggere una pipeline CI/CD;
- produrre un artifact;
- documentare una release;
- distinguere variabili e segreti;
- creare e versionare un'immagine container;
- collegare una versione applicativa ai segnali runtime;
- comprendere il ruolo di OpenTelemetry;
- leggere un trace semplice;
- ragionare su problemi introdotti da una release.

---

# Modulo 4
## Prometheus, Grafana, log centralizzati, strumenti enterprise e RCA

### Durata indicativa

```text
44 ore
11 sessioni da 4 ore
```

### Obiettivo del modulo

Lavorare con strumenti open source ed enterprise per metriche, dashboard, log, monitoraggio infrastrutturale e analisi degli incidenti.

### Argomenti principali

- Architettura degli strumenti di observability.
- Metriche applicative.
- Endpoint `/metrics`.
- Prometheus.
- Scrape.
- Target.
- Job.
- Time series.
- PromQL di base.
- Grafana.
- Datasource.
- Dashboard operative.
- Pannelli.
- Variabili.
- Alerting visuale.
- Log centralizzati.
- Log strutturati.
- Pipeline di ingestione.
- Parsing e normalizzazione.
- ELK / Elastic Stack.
- OpenSearch o strumenti equivalenti.
- Ricerca e analisi dei log.
- Zabbix o strumenti enterprise equivalenti.
- Monitoraggio host.
- Monitoraggio servizi.
- Trigger e notifiche.
- Strumenti enterprise e confronto operativo:
  - Splunk;
  - Dynatrace;
  - OpenText;
  - altri strumenti equivalenti, se disponibili.
- Incident investigation.
- Root Cause Analysis.
- Timeline dell'incidente.
- Runbook.
- Matrice decisionale degli strumenti.

### Competenze attese

Al termine del modulo dovremmo essere in grado di:

- esporre e interrogare metriche applicative;
- comprendere il modello di raccolta di Prometheus;
- creare dashboard operative in Grafana;
- distinguere dashboard utile e dashboard decorativa;
- comprendere il valore della centralizzazione dei log;
- cercare eventi significativi nei log;
- comprendere il ruolo degli strumenti enterprise;
- impostare una root cause analysis basata su evidenze.

---

# Modulo 5
## ML e AI applicati a dati osservabili

### Durata indicativa

```text
20 ore
5 sessioni da 4 ore
```

### Obiettivo del modulo

Introdurre l'uso di tecniche di analisi dati, Machine Learning e AI come supporto all'Observability.

Il modulo non ha l'obiettivo di trasformare il percorso in un corso completo di data science.  
L'obiettivo è capire come dati osservabili, metriche, log ed eventi possano essere usati per riconoscere pattern, anomalie e cambiamenti.

### Argomenti principali

- Dataset osservabili.
- Feature.
- Train/test.
- Metriche di valutazione.
- Baseline.
- Anomaly detection.
- Clustering.
- Trend.
- Forecasting.
- Drift di base.
- Riduzione del rumore.
- Correlazione eventi.
- Logging delle predizioni.
- Model observability di base.
- Rischi dell'automazione cieca.
- AI come supporto al ragionamento tecnico.

### Competenze attese

Al termine del modulo dovremmo essere in grado di:

- comprendere il valore dell'anomaly detection;
- distinguere soglie statiche e comportamento atteso;
- preparare un dataset semplice;
- leggere risultati di un modello semplice;
- riconoscere possibili falsi positivi e falsi negativi;
- usare strumenti AI come supporto all'analisi;
- mantenere controllo critico sui risultati.

---

# Modulo 6
## Project work finale, revisione e presentazione

### Durata indicativa

```text
16 ore
4 sessioni da 4 ore
```

### Obiettivo del modulo

Integrare le competenze acquisite in un progetto finale più compatto.

Il project work sarà orientato alla sintesi e alla presentazione di una soluzione, senza sottrarre troppo spazio ai moduli tecnici centrali.

### Possibili attività

- definizione dello scenario;
- backlog tecnico essenziale;
- architettura della soluzione;
- servizio o componente osservabile;
- pipeline minima o artifact;
- log, metriche e health check;
- dashboard o workbook;
- alert;
- mini incident drill;
- report finale;
- presentazione conclusiva.

### Output attesi

Il project work potrà includere:

```text
repository GitHub
codice o script
configurazioni
query
dashboard o screenshot
evidenze tecniche
report finale
presentazione conclusiva
```

### Competenze attese

Al termine del project work dovremmo essere in grado di:

- collegare più strumenti in un flusso coerente;
- produrre evidenze tecniche;
- spiegare le scelte fatte;
- presentare una soluzione di Observability;
- discutere limiti e miglioramenti;
- sostenere una revisione tecnica del lavoro prodotto.

---

# Mappa indicativa delle sessioni da 4 ore

La seguente mappa è indicativa e potrà essere adattata.

| Sessione | Ore | Focus |
|---|---:|---|
| S00 | 4h | Avvio corso, programma, GitHub Classroom, repository personale, primo push |
| S01 | 4h | Setup ambiente, metodo di lavoro, struttura repository |
| S02 | 4h | Linux filesystem, path, directory e file |
| S03 | 4h | File testuali, redirection, pipe e prime evidenze |
| S04 | 4h | Permessi, utenti, gruppi |
| S05 | 4h | Processi, servizi locali e troubleshooting |
| S06 | 4h | Rete, IP, DNS e porte |
| S07 | 4h | HTTP, endpoint e diagnostica |
| S08 | 4h | Log applicativi, log JSON e request ID |
| S09 | 4h | Health, readiness, metriche semplici e SLI |
| S10 | 4h | Azure foundations, tenant, subscription, Resource Group |
| S11 | 4h | Naming, tag, governance e cost control |
| S12 | 4h | Risorse Azure fondamentali e Activity Log |
| S13 | 4h | Diagnostica risorse Azure e metriche |
| S14 | 4h | Diagnostic settings e raccolta dati |
| S15 | 4h | Log Analytics Workspace |
| S16 | 4h | KQL base |
| S17 | 4h | KQL troubleshooting e aggregazioni |
| S18 | 4h | Alert rule e Action Group |
| S19 | 4h | Dashboard, workbook, revisione e cleanup |
| S20 | 4h | DevOps foundations, repository workflow e qualità |
| S21 | 4h | CI, test automatici e quality gate |
| S22 | 4h | Artifact, manifest e ambienti |
| S23 | 4h | Dockerfile, immagini container e tag |
| S24 | 4h | Container runtime, health e log |
| S25 | 4h | Pipeline multi-stage e deploy controllato |
| S26 | 4h | Smoke test, rollback e release-aware logging |
| S27 | 4h | Correlation ID, build ID e versione applicativa |
| S28 | 4h | OpenTelemetry introduttivo |
| S29 | 4h | Trace, span e context propagation |
| S30 | 4h | Incident response su pipeline e runbook |
| S31 | 4h | Architettura strumenti di observability |
| S32 | 4h | Prometheus e metriche applicative |
| S33 | 4h | PromQL base e target |
| S34 | 4h | Grafana datasource e dashboard |
| S35 | 4h | Grafana alerting e dashboard operative |
| S36 | 4h | Log centralizzati e log strutturati |
| S37 | 4h | ELK/OpenSearch o strumenti equivalenti |
| S38 | 4h | Zabbix o strumenti enterprise equivalenti |
| S39 | 4h | Tool enterprise: confronto operativo e casi d'uso |
| S40 | 4h | Incident investigation e timeline |
| S41 | 4h | Root Cause Analysis e runbook |
| S42 | 4h | Dataset osservabili e baseline |
| S43 | 4h | Anomaly detection |
| S44 | 4h | Clustering e correlazione eventi |
| S45 | 4h | Forecasting e riduzione rumore |
| S46 | 4h | AI come supporto all'analisi tecnica |
| S47 | 4h | Project work kickoff, scenario e backlog |
| S48 | 4h | Project work: architettura e implementazione minima |
| S49 | 4h | Project work: dashboard, alert o workbook |
| S50 | 4h | Project work: report, presentazione e revisione |
| S51 | 4h | Buffer tecnico e recupero argomenti critici |
| S52 | 4h | Consolidamento finale e simulazione scenario |
| S53 | 4h | Chiusura, retrospettiva, valutazione e cleanup |

---

# Nota sulla mappa delle sessioni

La mappa delle sessioni non è un vincolo rigido.

Alcune sessioni potranno essere:

- accorpate;
- alleggerite;
- approfondite;
- usate come recupero;
- adattate agli ambienti disponibili;
- riorientate verso il project work.

La priorità sarà mantenere continuità tra:

```text
concetti
→ laboratorio
→ evidenze
→ report
→ discussione tecnica
```

---

# Competenze trasversali

Durante tutto il percorso lavoreremo anche su competenze trasversali:

- metodo di troubleshooting;
- scrittura di report tecnici;
- uso consapevole di Git;
- documentazione delle evidenze;
- ragionamento per ipotesi;
- lettura critica dei dati;
- comunicazione tecnica;
- lavoro individuale e di gruppo;
- autonomia operativa;
- attenzione alla sicurezza dei dati.

---

# Strumenti che potranno essere utilizzati

L'elenco seguente è indicativo.

Non tutti gli strumenti saranno necessariamente usati con lo stesso livello di approfondimento.

| Area | Strumenti possibili |
|---|---|
| Versionamento | Git, GitHub, GitHub Classroom |
| Sistema operativo | Linux, shell, PowerShell |
| Scripting | Bash, Python |
| Cloud | Microsoft Azure |
| Monitoraggio cloud | Azure Monitor, Log Analytics |
| Query | KQL, PromQL |
| CI/CD | GitHub Actions, Azure Pipelines |
| Container | Docker, registry, runtime cloud |
| Telemetria | OpenTelemetry |
| Metriche | Prometheus |
| Dashboard | Grafana, Azure Workbook |
| Log | Elastic/OpenSearch o strumenti equivalenti |
| Monitoring enterprise | Zabbix o strumenti equivalenti |
| AI/ML | strumenti e librerie di supporto all'analisi |

---

# Come saranno valutate le attività

La valutazione formativa terrà conto di:

- partecipazione ai laboratori;
- correttezza tecnica delle attività;
- qualità delle evidenze prodotte;
- chiarezza dei report;
- uso corretto del repository GitHub;
- capacità di spiegare le scelte;
- capacità di diagnosticare problemi;
- autonomia crescente;
- project work finale.

La valutazione non sarà basata solo sul risultato finale, ma anche sul percorso seguito.

---

# Cosa ci si aspetta dai partecipanti

Durante il corso sarà importante:

- lavorare con continuità;
- salvare spesso il lavoro;
- fare commit leggibili;
- non aspettare la fine della giornata per segnalare problemi;
- documentare errori e soluzioni;
- produrre evidenze;
- partecipare ai momenti di confronto;
- non salvare mai segreti reali nel repository;
- mantenere ordinata la propria area di lavoro.

---

# Nota finale sul programma

Il programma presentato è una guida complessiva del percorso.

Potrà essere adattato in base a:

- tempo effettivo disponibile;
- livello di partenza del gruppo;
- disponibilità degli ambienti tecnici;
- necessità di consolidamento;
- difficoltà emerse nei laboratori;
- priorità didattiche;
- obiettivi finali del project work.

La priorità sarà acquisire un metodo concreto per osservare, diagnosticare, documentare e migliorare sistemi tecnici.

Non è necessario memorizzare tutti gli strumenti.  
È necessario imparare a ragionare sui segnali, formulare ipotesi e produrre evidenze.
