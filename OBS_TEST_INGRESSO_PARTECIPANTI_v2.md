# Academy Observability
# Test di ingresso - versione 2

## Scopo del test

Questo test ha lo scopo di rilevare le competenze in ingresso dei partecipanti prima dell'inizio del percorso.

Il test **non ha finalità valutativa o selettiva**.  
Serve a costruire un punto di partenza misurabile, utile per confrontare le competenze iniziali con quelle acquisite al termine del corso.

Il risultato aiuterà il docente a calibrare il livello di approfondimento dei diversi argomenti.

---

## Istruzioni

- Il test contiene **30 domande**.
- Ogni domanda ha **3 risposte possibili**.
- Per ogni domanda indicare una sola risposta: **A, B oppure C**.
- Non usare strumenti esterni durante la compilazione.
- In caso di dubbio, scegliere la risposta che sembra più corretta.

Tempo consigliato:

```text
35 - 45 minuti
```

---

## Scheda partecipante

Compilare prima di iniziare.

| Campo | Risposta |
|---|---|
| Nome e cognome | |
| Data | |
| Esperienza precedente in IT | nessuna / base / intermedia / avanzata |
| Esperienza precedente con Linux | nessuna / base / intermedia / avanzata |
| Esperienza precedente con cloud | nessuna / base / intermedia / avanzata |
| Esperienza precedente con DevOps | nessuna / base / intermedia / avanzata |
| Esperienza precedente con monitoring/observability | nessuna / base / intermedia / avanzata |

---

# Domande

## 1. Git e repository

### 1. Che cosa fa il comando `git clone`?

A. Inizializza un repository Git vuoto nella cartella corrente  
B. Crea una copia locale di un repository remoto già esistente  
C. Invia al repository remoto le modifiche già committate localmente

---

### 2. Che cosa indica normalmente `git status`?

A. La cronologia completa dei commit del repository locale  
B. L'elenco dei repository remoti associati al progetto  
C. Lo stato dei file modificati, aggiunti, tracciati o non tracciati

---

### 3. Qual è lo scopo principale di un commit?

A. Spostare file modificati dall'area di lavoro alla staging area  
B. Registrare nella cronologia una versione coerente delle modifiche  
C. Sincronizzare automaticamente il repository locale con GitHub

---

## 2. Linux e shell

### 4. In un sistema Linux, che cosa rappresenta normalmente il percorso `/var/log`?

A. Una directory usata spesso per contenere file di log di sistema e servizi  
B. Una directory temporanea svuotata a ogni comando eseguito dall'utente  
C. Una directory che contiene solo file binari essenziali del sistema

---

### 5. Che cosa fa il comando `ls -la`?

A. Mostra solo i file modificati più di recente nella directory corrente  
B. Mostra i processi attivi con informazioni dettagliate  
C. Mostra file e directory con dettagli, includendo anche elementi nascosti

---

### 6. In Linux, che cosa rappresentano i permessi `rwx`?

A. Lettura, scrittura ed esecuzione  
B. Ricerca, workdir ed export  
C. Readiness, warning ed execution

---

## 3. Processi, servizi e troubleshooting locale

### 7. Che cosa identifica un PID?

A. Una porta usata da un servizio di rete  
B. Un processo in esecuzione sul sistema  
C. Il percorso assoluto di un file di log

---

### 8. Perché può essere utile verificare quali processi sono in ascolto su una porta?

A. Per capire quale utente ha creato un file nella directory corrente  
B. Per modificare automaticamente la configurazione DNS del sistema  
C. Per capire quale servizio sta usando una porta o se un servizio è raggiungibile

---

### 9. Quale approccio è più corretto durante un troubleshooting?

A. Riavviare subito il servizio e considerare risolto il problema se sparisce temporaneamente  
B. Partire dal sintomo, formulare ipotesi, verificarle e documentare le evidenze  
C. Applicare più correzioni insieme per ridurre il tempo di diagnosi

---

## 4. Rete e HTTP

### 10. Che cosa rappresenta una porta TCP?

A. Un punto logico di comunicazione usato da un processo o servizio di rete  
B. L'indirizzo fisico della scheda di rete espresso in formato numerico  
C. Il nome simbolico associato a un host tramite DNS

---

### 11. Che cosa indica generalmente un codice HTTP `200`?

A. La richiesta è stata ricevuta ma richiede autenticazione  
B. La risorsa richiesta è stata spostata in modo permanente  
C. La richiesta è stata gestita correttamente

---

### 12. Che cosa indica generalmente un codice HTTP `500`?

A. Il client ha inviato una richiesta formalmente non valida  
B. Il server ha incontrato un errore durante la gestione della richiesta  
C. La risorsa richiesta non è stata trovata

---

## 5. Log, metriche e segnali osservabili

### 13. Qual è lo scopo principale di un log applicativo?

A. Registrare eventi significativi prodotti dall'applicazione durante l'esecuzione  
B. Misurare sempre in modo numerico il consumo di CPU e memoria  
C. Sostituire la documentazione tecnica e i commenti nel codice

---

### 14. Quale tra questi è un esempio di metrica?

A. Una riga di log con messaggio di errore e timestamp  
B. Un identificativo univoco associato a una richiesta HTTP  
C. Il numero di richieste HTTP ricevute in un intervallo di tempo

---

### 15. Perché può essere utile un `request-id`?

A. Per indicare quale versione di Git è installata sul server  
B. Per correlare log ed eventi relativi alla stessa richiesta  
C. Per assegnare automaticamente un indirizzo IP al client

---

## 6. Health, readiness e SLI

### 16. Qual è lo scopo tipico di un endpoint `/health`?

A. Indicare se il servizio è vivo o almeno raggiungibile  
B. Esporre sempre tutte le metriche interne del servizio  
C. Verificare che ogni dipendenza esterna sia pronta per il traffico

---

### 17. Qual è la differenza generale tra health e readiness?

A. Health riguarda solo servizi HTTP, readiness solo database relazionali  
B. Health indica se il servizio è vivo; readiness se è pronto a ricevere traffico  
C. Health e readiness sono sempre sinonimi e vengono usati senza distinzione

---

### 18. Che cosa rappresenta uno SLI?

A. Una soglia contrattuale che impone una penale economica  
B. Un file di configurazione usato per definire alert in Grafana  
C. Un indicatore misurabile del livello di servizio

---

## 7. Cloud e Azure

### 19. In Azure, che cosa è un Resource Group?

A. Un contenitore logico per organizzare e gestire risorse correlate  
B. Un gruppo di utenti che hanno sempre gli stessi permessi amministrativi  
C. Un servizio usato esclusivamente per interrogare log applicativi

---

### 20. A cosa servono i tag applicati alle risorse cloud?

A. A modificare automaticamente la dimensione delle risorse quando aumenta il traffico  
B. A impedire la cancellazione accidentale di qualsiasi risorsa del tenant  
C. A classificare e organizzare risorse tramite coppie chiave-valore

---

### 21. Che cosa contiene tipicamente l'Activity Log di Azure?

A. Le righe di log applicativo prodotte direttamente dal codice del servizio  
B. Eventi e operazioni di gestione effettuate sulle risorse Azure  
C. Le metriche di latenza raccolte ogni secondo da tutte le applicazioni

---

## 8. Log Analytics, KQL, alert e dashboard

### 22. A cosa serve un Log Analytics Workspace?

A. A raccogliere e interrogare dati di log e telemetria tramite query  
B. A distribuire automaticamente nuove versioni dell'applicazione  
C. A creare immagini container partendo da un Dockerfile

---

### 23. In KQL, quale operatore viene usato normalmente per filtrare righe?

A. `project`  
B. `summarize`  
C. `where`

---

### 24. Quale caratteristica dovrebbe avere un buon alert operativo?

A. Deve scattare ogni volta che viene scritto un log, così non si perde nulla  
B. Deve essere comprensibile, azionabile e non eccessivamente rumoroso  
C. Deve basarsi preferibilmente su una sola metrica senza contesto temporale

---

## 9. DevOps, CI/CD e container

### 25. Che cosa indica Continuous Integration?

A. La distribuzione automatica in produzione senza alcun controllo manuale  
B. Il monitoraggio continuo della CPU di una macchina virtuale  
C. L'integrazione frequente delle modifiche con controlli automatici

---

### 26. Che cosa è un artifact in una pipeline?

A. Un output prodotto dalla pipeline, come un pacchetto, un report o un'immagine  
B. Un file temporaneo che non deve mai essere conservato o scaricato  
C. Una variabile segreta usata per autenticarsi verso un servizio esterno

---

### 27. Che cosa rappresenta un'immagine container?

A. Un archivio contenente solo i file di log prodotti dal container  
B. Un pacchetto eseguibile che contiene applicazione e dipendenze necessarie  
C. Una fotografia dello stato corrente della dashboard di monitoraggio

---

## 10. OpenTelemetry, tracing, Prometheus, Grafana, RCA e AI

### 28. Che cosa descrive un trace in un sistema distribuito?

A. L'elenco dei processi attivi su una singola macchina  
B. Il contenuto completo di una tabella di metriche  
C. Il percorso di una richiesta attraverso uno o più componenti

---

### 29. Qual è il ruolo principale di Prometheus?

A. Raccogliere e interrogare metriche time-series  
B. Gestire repository Git e pull request  
C. Eseguire automaticamente il deploy di container in produzione

---

### 30. In un'analisi di incidente, che cosa si intende per Root Cause Analysis?

A. La raccolta di tutti i log disponibili senza formulare ipotesi  
B. Un processo per individuare la causa radice di un problema sulla base di evidenze  
C. La configurazione di una dashboard con molti grafici di sistema

---

# Griglia risposte partecipante

Compilare con A, B oppure C.

| Domanda | Risposta |
|---:|---|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
| 5 | |
| 6 | |
| 7 | |
| 8 | |
| 9 | |
| 10 | |
| 11 | |
| 12 | |
| 13 | |
| 14 | |
| 15 | |
| 16 | |
| 17 | |
| 18 | |
| 19 | |
| 20 | |
| 21 | |
| 22 | |
| 23 | |
| 24 | |
| 25 | |
| 26 | |
| 27 | |
| 28 | |
| 29 | |
| 30 | |

---

## Autovalutazione finale

Compilare dopo aver risposto alle domande.

| Domanda | Risposta |
|---|---|
| Quali argomenti conoscevo già meglio? | |
| Quali argomenti mi sembrano più nuovi? | |
| Quali strumenti ho già usato almeno una volta? | |
| Quale area vorrei consolidare di più durante il corso? | |
