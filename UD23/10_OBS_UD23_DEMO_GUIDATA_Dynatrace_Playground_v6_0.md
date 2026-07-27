# OBS UD23 - Demo guidata pratica
# Dynatrace Playground: Services, dipendenze, log e tracing

## 0. Perché questa attività

Finora Dynatrace è stato collocato nella comparativa come piattaforma enterprise di Observability/APM. In questa attività lo usiamo **davvero**, senza installare agenti e senza modificare l'app Catalogo prodotti.

Useremo il **Dynatrace Playground**, un ambiente sandbox ufficiale con dati di esempio già disponibili.

L'obiettivo non è imparare ad amministrare Dynatrace. L'obiettivo è riconoscere nella pratica concetti già studiati:

```text
servizio
  -> endpoint
     -> metriche di salute
        -> dipendenze
           -> infrastruttura
              -> log
                 -> trace distribuite
```

**Durata indicativa: 25-30 minuti.**

> Nota: l'interfaccia Dynatrace evolve nel tempo. I nomi di alcune voci possono cambiare leggermente; segui il concetto indicato nel passo, non memorizzare la posizione grafica di un pulsante.

---

## 1. Prerequisiti

Servono:

- browser con accesso Internet;
- account gratuito per accedere al Playground;
- nessuna installazione locale;
- nessun OneAgent obbligatorio;
- nessuna modifica ai container del corso.

Percorso consigliato:

```text
https://www.dynatrace.com/try-free/
-> Explore Playground
```

La documentazione ufficiale descrive il Playground come sandbox preconfigurata con dati di esempio, utilizzabile senza installazione o ingestion propria.

---

## 2. Prima osservazione: Services Explorer

Apri Dynatrace Playground e cerca l'applicazione:

```text
Services
```

Apri la vista di esplorazione dei servizi (**Explorer** o vista equivalente).

Osserva che Dynatrace presenta i servizi come entità già correlate con indicatori operativi.

Cerca almeno questi indicatori:

```text
Response time
Throughput
Failure rate
Health / alert status
```

### Domanda 1

Confronta questa vista con Prometheus/Grafana:

```text
Prometheus/Grafana
-> siamo noi a scegliere metriche e costruire query/dashboard

Dynatrace
-> parte dal servizio come entità osservabile e collega più viste
```

Annota nel file `work/UD23/docs/evidence_ud23.md` una differenza che hai osservato.

---

## 3. Filtrare un'applicazione distribuita

Nel campo di filtro dei servizi prova a restringere la vista al namespace di esempio:

```text
k8s.namespace.name = astroshop
```

Se il dataset del Playground è stato aggiornato e il filtro non restituisce dati, scegli un namespace o un gruppo di servizi disponibile nella vista corrente.

L'obiettivo è ottenere un insieme di servizi appartenenti alla stessa applicazione distribuita.

### Cosa osservare

Non guardare solo i nomi.

Chiediti:

```text
Quanti servizi compongono l'applicazione?
Quali mostrano failure rate maggiore?
Quali hanno response time maggiore?
Esistono alert o problemi associati?
```

---

## 4. Drill-down su un servizio

Se disponibile, seleziona:

```text
recommendation service
```

oppure un altro servizio applicativo visibile nel Playground.

Apri il dettaglio del servizio e osserva la vista **Overview**.

Individua:

- response time;
- throughput;
- failure rate;
- elenco degli endpoint/request.

### Domanda 2

Quale concetto già visto nelle UD precedenti ritrovi qui?

Risposta attesa:

```text
Le stesse domande operative:
quanto traffico?
quanto è lento?
quanti errori?
quale endpoint è coinvolto?
```

La differenza non è la domanda: cambia il livello di integrazione dello strumento.

---

## 5. Endpoint: dal servizio alla singola operazione

Scorri fino alla sezione degli **Endpoints**.

Scegli un endpoint e osserva, quando disponibili:

```text
response time
throughput
failure rate
```

### Confronto con il laboratorio Catalogo prodotti

Nel nostro percorso abbiamo usato:

```text
/products
/products/slow
/products/error
```

Dynatrace applica la stessa logica a un ambiente più ampio:

```text
servizio
  -> endpoint/request
      -> performance
      -> errori
      -> dipendenze
```

Annota un endpoint osservato e una metrica utile.

---

## 6. Dal servizio all'infrastruttura

Nel dettaglio del servizio cerca la sezione o tab:

```text
Infrastructure
```

Osserva le entità associate, per esempio:

```text
pod
process
host
cluster
```

### Domanda 3

Perché questa vista è importante?

Perché permette di passare da:

```text
"il servizio è lento"
```

alla domanda:

```text
"dove sta girando il servizio e quali risorse lo sostengono?"
```

Questo è un esempio concreto di **correlazione tra applicazione e infrastruttura**.

---

## 7. Correlare i log

Apri la sezione:

```text
Logs
```

Cerca errori, warning o messaggi collegati al servizio nel periodo selezionato.

Nota il vantaggio operativo:

```text
non parto da tutti i log dell'azienda
-> parto dal servizio che sto investigando
-> restringo automaticamente il contesto
-> cerco i messaggi pertinenti
```

### Confronto

```text
Log stack tradizionale
-> cerco e filtro gli eventi

Dynatrace
-> posso arrivare ai log partendo dal contesto del servizio
```

Non significa che uno sia sempre migliore dell'altro: significa che il **contesto di navigazione** è diverso.

---

## 8. Dipendenze e trace distribuite

Dal servizio cerca una vista relativa a:

```text
Service flow
Related services
Distributed Traces
Trace
```

La terminologia o il punto di accesso può variare con la versione dell'interfaccia.

Osserva almeno una relazione:

```text
servizio A
   -> chiama
servizio B
   -> eventualmente chiama
servizio C / database / servizio esterno
```

Poi apri, quando disponibile, una trace distribuita.

Ricorda:

```text
trace = percorso di una singola richiesta
span  = singolo tratto/operazione del percorso
```

### Confronto con Jaeger

```text
Jaeger
-> molto focalizzato sul distributed tracing
-> leggiamo trace e span

Dynatrace
-> tracing inserito in una piattaforma più ampia
-> servizio + metriche + dipendenze + infra + log + trace
```

Questa è la differenza da comprendere: **non che Dynatrace “sostituisca” automaticamente Jaeger, ma che integra più segnali e contesti nella stessa piattaforma**.

---

## 9. Evidenza da produrre

Nel file:

```text
work/UD23/docs/evidence_ud23.md
```

aggiungi:

```markdown
## Dynatrace Playground

- Servizio osservato:
- Indicatore osservato (response time / throughput / failure rate):
- Endpoint osservato:
- Dipendenza o relazione individuata:
- Evidenza da log o trace:
- Una differenza rispetto a Prometheus/Grafana:
- Una differenza rispetto a Jaeger:
```

Puoi aggiungere uno screenshot, se consentito dall'ambiente del corso.

---

## 10. Mini-verifica finale

Completa queste frasi:

```text
Prometheus mi aiuta soprattutto a ____________________________________

Grafana mi aiuta soprattutto a ______________________________________

Jaeger mi aiuta soprattutto a _______________________________________

Dynatrace mi ha mostrato in modo integrato ___________________________
```

La risposta non deve essere una classifica.

Deve dimostrare che hai capito **quale domanda operativa ogni vista aiuta a risolvere**.

---

## 11. Estensione facoltativa - usare dati propri

Questa parte **non è necessaria per completare UD23**.

Chi vuole approfondire può creare un ambiente trial Dynatrace e collegare un proprio host tramite OneAgent seguendo la procedura ufficiale mostrata nel proprio tenant.

Schema concettuale:

```text
Host / VM / ambiente supportato
        |
        | OneAgent o integrazione OpenTelemetry
        v
Dynatrace environment
        |
        +--> Services
        +--> Metrics
        +--> Logs
        +--> Distributed traces
        +--> Infrastructure
```

Non copiare token o URL di ambiente nei repository Git.

Non usare questa estensione come prerequisito per la lezione: configurazione, privilegi e modalità di installazione dipendono dall'ambiente.

---

## 12. Cosa puoi dichiarare dopo questa attività

Dopo la demo puoi correttamente dire:

```text
Ho svolto una esplorazione pratica guidata di Dynatrace Playground,
analizzando service health, endpoint, dipendenze, infrastruttura,
log e distributed tracing su dati di esempio.
```

Non è ancora corretto dichiarare:

```text
Amministrazione avanzata Dynatrace
Deployment enterprise Dynatrace
Progettazione completa licensing/retention Dynatrace
```

La precisione nel descrivere il livello di esperienza è parte della competenza professionale.

---

## Riferimenti ufficiali verificati il 24/07/2026

- Dynatrace - Get started: https://docs.dynatrace.com/docs/discover-dynatrace/get-started
- Dynatrace - Discover / Playground: https://docs.dynatrace.com/docs/discover-dynatrace
- Dynatrace - Manage service health and performance: https://docs.dynatrace.com/docs/observe/application-observability/services/managing-service-health
- Dynatrace - Services: https://docs.dynatrace.com/docs/observe/application-observability/services
- Dynatrace - Distributed tracing: https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing
