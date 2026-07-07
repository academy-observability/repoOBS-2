# OBS UD11 - Concetti
## DevOps, Azure DevOps e architettura del flusso CI/CD cloud

Versione: v5.5  
Destinatari: partecipanti  
Durata consigliata: 4 ore mattina, inclusa discussione guidata  
Collocazione nel percorso: dopo UD10 e prima della parte Docker/CI/CD operativa

---

# 1. Perché questa UD esiste

Nelle UD precedenti abbiamo già lavorato su Azure, risorse cloud, Log Analytics, KQL, monitoraggio, alert e osservabilità.

In UD05, in particolare, il deployment o la creazione di risorse Azure è stato affrontato in modo prevalentemente manuale: portale, CLI, verifica delle risorse, controllo dello stato e uso dei servizi già creati.

Da UD11 in poi cambia il punto di vista.

Non vogliamo più ragionare solo così:

```text
Creo o modifico una risorsa a mano
Verifico se funziona
Raccolgo evidenza
```

Vogliamo iniziare a ragionare così:

```text
Modifico codice o configurazione
Versiono la modifica
Una pipeline esegue passaggi ripetibili
La pipeline costruisce un risultato distribuibile
Il risultato viene pubblicato in un registry
Il deploy viene eseguito in modo automatico
Il sistema viene verificato e osservato
```

Questa UD serve a costruire la base concettuale e operativa per questo passaggio.

---

# 2. Obiettivo della UD11

Alla fine della UD11 dobbiamo saper spiegare:

- che cos'è DevOps;
- quale problema cerca di risolvere;
- che cosa significano CI e CD;
- che cos'è una pipeline;
- perché codice, artifact, immagini e registry non sono la stessa cosa;
- che cos'è Azure DevOps;
- perché nel corso useremo GitHub come repository del codice;
- perché useremo Azure DevOps soprattutto come motore CI/CD;
- dove si collocano ACR, ACI, Azure Container Apps, Azure Monitor, Application Insights e Log Analytics;
- quale sarà il flusso tecnico generale che useremo nelle attività successive.

Alla fine della UD11 dobbiamo inoltre avere pronto almeno il contenitore operativo minimo:

```text
Organizzazione Azure DevOps
Progetto Azure DevOps
Accesso a Pipelines
Accesso a Project settings
Consapevolezza del punto in cui verranno create le service connection
```

In questa UD non costruiamo ancora immagini Docker e non facciamo ancora deploy automatici.

---

# 3. DevOps: definizione pratica

DevOps non è un prodotto, non è una pipeline e non è semplicemente usare Docker o Azure.

DevOps è un modo di organizzare il ciclo di vita del software per ridurre la distanza tra:

- sviluppo;
- test;
- rilascio;
- operations;
- monitoraggio;
- feedback.

In pratica DevOps prova a rispondere a questa domanda:

```text
Come facciamo a portare una modifica dal codice a un ambiente eseguibile in modo più rapido, controllato, tracciabile e verificabile?
```

La risposta non è solo tecnica. Include persone, processo, responsabilità, automazione, standard e feedback.

---

# 4. Il problema del modello tradizionale

Nel modello tradizionale, spesso il lavoro procede a blocchi separati:

```text
Analisi
  ->
Sviluppo
  ->
Test
  ->
Rilascio
  ->
Esercizio
```

Il problema è che ogni passaggio può diventare un collo di bottiglia.

Esempi tipici:

- il codice funziona sul PC dello sviluppatore ma non nell'ambiente reale;
- il deploy viene eseguito a mano e cambia ogni volta;
- i test vengono fatti tardi;
- gli errori emergono solo dopo il rilascio;
- nessuno sa con precisione quale versione sia stata distribuita;
- se qualcosa va male, il rollback non è chiaro;
- il team operations riceve il software senza abbastanza contesto.

DevOps nasce per ridurre questi attriti.

---

# 5. Il ciclo DevOps semplificato

Per il nostro percorso useremo questa mappa mentale:

```text
Pianificazione
   ->
Codice
   ->
Versionamento
   ->
Build
   ->
Test
   ->
Packaging / immagine
   ->
Registry
   ->
Deploy
   ->
Verifica
   ->
Osservabilità
   ->
Feedback
```

Questa mappa è importante perché ci evita di confondere gli strumenti.

Ogni strumento ha un ruolo preciso.

---

# 6. CI e CD

## 6.1 CI - Continuous Integration

La CI riguarda l'integrazione continua delle modifiche.

In termini semplici:

```text
Ogni volta che il codice cambia, una procedura automatica controlla che almeno le verifiche minime siano superate.
```

Una pipeline CI può eseguire:

- checkout del codice;
- controllo sintassi;
- installazione dipendenze;
- test automatici;
- build;
- creazione di un artifact;
- creazione di una immagine container.

La CI risponde a domande come:

- il codice si integra correttamente?
- la build passa?
- i test minimi passano?
- il risultato prodotto è coerente?

## 6.2 CD - Continuous Delivery

La CD riguarda la consegna o il deployment controllato del software.

In termini semplici:

```text
Ciò che è stato costruito e verificato viene portato in un ambiente di destinazione in modo ripetibile.
```

Una pipeline CD può eseguire:

- recupero artifact o immagine;
- autenticazione verso Azure;
- deploy su un servizio;
- impostazione variabili d'ambiente;
- smoke test;
- raccolta log;
- produzione di evidenze.

La CD risponde a domande come:

- il software può essere distribuito?
- il deploy è ripetibile?
- dopo il deploy il servizio risponde davvero?
- sappiamo quale versione è in esecuzione?

---

# 7. Che cos'è una pipeline

Una pipeline è una sequenza automatizzata di passaggi.

Nel nostro percorso una pipeline potrà fare cose come:

```text
Leggere codice da GitHub
Eseguire controlli
Costruire una immagine Docker
Pubblicare l'immagine su ACR
Distribuire il container su Azure
Eseguire smoke test
Mostrare log e revisioni
```

La pipeline è utile perché rende il processo:

- ripetibile;
- leggibile;
- tracciabile;
- verificabile;
- meno dipendente da passaggi manuali.

Una pipeline non è automaticamente buona solo perché è automatica.

Una pipeline deve essere anche chiara, manutenibile e coerente con l'obiettivo del rilascio.

---

# 8. Repository, artifact, immagine e registry

Questa distinzione è essenziale.

## 8.1 Repository del codice

È il luogo in cui vive il codice sorgente.

Nel nostro percorso:

```text
GitHub = repository del codice
```

Dentro GitHub troveremo:

- codice applicativo;
- Dockerfile;
- file YAML della pipeline;
- documentazione;
- evidenze;
- configurazioni non segrete.

## 8.2 Artifact

Un artifact è un risultato prodotto da una build.

Può essere:

- un file `.zip`;
- un package;
- una libreria;
- un eseguibile;
- una immagine container.

L'artifact non è il codice sorgente: è un prodotto generato a partire dal codice.

## 8.3 Immagine container

Una immagine container è un pacchetto eseguibile che contiene applicazione, runtime e dipendenze.

Nelle prossime UD impareremo a costruirla con Docker.

In UD11 ci basta capire il ruolo:

```text
Codice sorgente -> Build -> Immagine container
```

## 8.4 Registry immagini

Un registry immagini è il luogo in cui vengono archiviate le immagini container.

Nel nostro percorso:

```text
ACR = Azure Container Registry
```

Quindi la separazione corretta è:

```text
GitHub contiene codice
ACR contiene immagini
Azure esegue il deploy
Azure DevOps automatizza il processo
```

---

# 9. Che cos'è Azure DevOps

Azure DevOps è una suite Microsoft per supportare pianificazione, codice, build, test e deploy.

Include diversi moduli:

- Azure Boards;
- Azure Repos;
- Azure Pipelines;
- Azure Test Plans;
- Azure Artifacts.

Nel nostro percorso non useremo tutta la suite nello stesso modo.

Il punto centrale sarà:

```text
Azure Pipelines
```

---

# 10. Perché GitHub resta il repository del codice

I partecipanti stanno già lavorando con Git e GitHub.

Non avrebbe senso cambiare repository sorgente proprio mentre introduciamo DevOps.

Quindi useremo questo modello:

```text
GitHub = repository codice
Azure DevOps Pipelines = CI/CD
ACR = registry immagini
Azure = target di deploy
```

Questo modello è importante perché mostra un caso reale abbastanza comune: strumenti diversi svolgono ruoli diversi nello stesso ciclo DevOps.

Non è necessario usare Azure Repos per usare Azure Pipelines.

---

# 11. Azure DevOps come motore CI/CD

Nel nostro percorso Azure DevOps servirà soprattutto a:

- leggere il codice da GitHub;
- eseguire pipeline;
- costruire immagini;
- pubblicarle in ACR;
- distribuire servizi su Azure;
- eseguire controlli post-deploy.

In UD11 non costruiamo ancora pipeline operative di deploy.

Prepariamo però il contesto:

- organizzazione;
- progetto;
- permessi;
- sezione Pipelines;
- sezione Project settings;
- concetto di service connection.

---

# 12. Che cosa sono le service connection

Una service connection è una connessione configurata in Azure DevOps per permettere alle pipeline di autenticarsi verso sistemi esterni.

Nel nostro percorso ne incontreremo soprattutto due tipi:

## 12.1 Connessione verso GitHub

Serve alla pipeline Azure DevOps per leggere il repository GitHub.

## 12.2 Connessione verso Azure Resource Manager

Serve alla pipeline per operare su risorse Azure, per esempio:

- ACR;
- ACI;
- Azure Container Apps;
- Log Analytics;
- Application Insights.

In UD11 non è obbligatorio completare tutte le connessioni.

È però necessario sapere dove si trovano:

```text
Project settings -> Service connections
```

---

# 13. Docker locale e Docker nel ciclo Azure

Questa UD introduce il ruolo di Docker, ma non lo usa operativamente.

La distinzione concettuale è questa:

| Livello | Significato |
|---|---|
| Docker locale | Costruire e avviare container sul proprio ambiente per capire immagine, container, porta, log e smoke test. |
| Docker in pipeline | Lasciare che sia una pipeline a eseguire build e pubblicazione dell'immagine. |
| ACR | Conservare immagini container e relativi tag in un registry Azure. |
| ACI | Eseguire rapidamente un container singolo in Azure per un primo deploy semplice. |
| Azure Container Apps | Distribuire servizi containerizzati più strutturati, ad esempio frontend e backend separati. |

Frase chiave:

```text
In locale impariamo che cos'è un container e come si comporta.
In Azure impariamo come quel container entra in una pipeline, viene pubblicato in un registry e viene distribuito automaticamente.
```

---

# 14. Architettura complessiva del flusso

La progressione tecnica generale sarà questa:

```text
Fondamenti DevOps
   ->
Docker locale
   ->
Pipeline e registry
   ->
Primo deploy cloud semplice
   ->
Applicazione frontend/backend
   ->
Deploy cloud più maturo
   ->
Observability post-deploy
```

Questa non è una sequenza rigida di UD.  
È una mappa concettuale del percorso tecnico: il docente potrà modificarne la distribuzione senza cambiare il significato del flusso.

---

# 15. Mappa architetturale del modulo DevOps

La mappa generale è questa:

```text
Codice sorgente
   |
   v
GitHub
   |
   v
Azure DevOps Pipelines
   |
   +--> Build container image
   +--> Push image to Azure Container Registry
   |
   v
Azure deployment target
   |
   +--> primo livello: Azure Container Instances
   |
   +--> livello più maturo: Azure Container Apps
   |
   v
Applicazione in esecuzione
   |
   v
Observability in Azure
   |
   +--> Application Insights
   +--> Azure Monitor
   +--> Log Analytics
```

In UD11 dobbiamo solo saper leggere questa mappa e spiegare il ruolo di ciascun blocco.

---

# 16. Errori concettuali da evitare

## 16.1 “DevOps significa usare una pipeline”

No.

La pipeline è uno strumento. DevOps è un modo di collegare processo, automazione, verifica e feedback.

## 16.2 “GitHub e ACR fanno la stessa cosa”

No.

```text
GitHub = codice
ACR = immagini container
```

## 16.3 “Azure DevOps obbliga a usare Azure Repos”

No.

Nel nostro corso il codice resta su GitHub.

## 16.4 “Deploy riuscito significa lavoro finito”

No.

Dopo il deploy servono verifica, log, metriche, tracing e osservabilità.

## 16.5 “Docker locale e deploy Azure sono la stessa cosa”

No.

Docker locale serve a capire e testare il container.

Il deploy Azure serve a eseguire quella immagine in una piattaforma cloud.

---

# 17. Mini glossario

## DevOps

Approccio che collega sviluppo, test, rilascio, operations e feedback attraverso processi e automazione.

## CI

Continuous Integration: integrazione e verifica automatica delle modifiche.

## CD

Continuous Delivery: distribuzione controllata e ripetibile di ciò che è stato costruito.

## Pipeline

Sequenza automatizzata di passaggi.

## Repository

Luogo in cui vive il codice sorgente.

## Artifact

Risultato prodotto da una build.

## Container image

Pacchetto eseguibile che contiene applicazione, runtime e dipendenze.

## Registry

Archivio delle immagini container.

## ACR

Azure Container Registry: registry immagini Azure.

## ACI

Azure Container Instances: primo target cloud semplice per container singolo.

## Azure Container Apps

Servizio Azure più adatto per applicazioni containerizzate composte da più servizi.

## Application Insights

Componente di Azure Monitor per telemetria applicativa.

## Log Analytics

Ambiente di interrogazione dei dati tramite query KQL.

---

# 18. Cosa dobbiamo saper dire alla fine

Alla fine della parte concettuale dobbiamo essere in grado di dire:

```text
UD05 mi ha fatto vedere il cloud in modo manuale.
UD11 mi fa capire il ciclo DevOps che automatizzerà progressivamente quel lavoro.
GitHub contiene il codice.
Azure DevOps esegue le pipeline.
ACR contiene le immagini.
ACI e Azure Container Apps eseguono i container.
Application Insights, Azure Monitor e Log Analytics permettono di osservare ciò che è stato distribuito.
```

Questa è la base per affrontare le UD successive senza ridurre i laboratori a una sequenza meccanica di comandi.
