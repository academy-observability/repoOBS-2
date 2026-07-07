# OBS UD11 - Mini-attività
## Mappa del flusso DevOps cloud prima dei comandi

Versione: v5.5.1  
Destinatari: partecipanti  
Durata consigliata: 45-60 minuti  
Tipo attività: attività concettuale guidata

---

# 1. Obiettivo

Prima di usare comandi, pipeline e servizi Azure, dobbiamo saper leggere il flusso complessivo.

Questa attività serve a verificare se hai capito il ruolo dei componenti principali:

- GitHub;
- Azure DevOps Pipelines;
- Azure Container Registry;
- Azure Container Instances;
- Azure Container Apps;
- Application Insights;
- Azure Monitor;
- Log Analytics.

La mini-attività non chiede di memorizzare la sequenza delle UD successive.  
La sequenza didattica potrà essere aggiornata dal docente. Qui ci interessa capire i ruoli tecnici dei componenti.

---

# 2. Scenario

Il docente presenta questa catena logica generale:

```text
Codice sorgente
   |
   v
Repository del codice
   |
   v
Pipeline CI/CD
   |
   +--> Build
   +--> Test
   +--> Packaging / immagine
   +--> Pubblicazione artifact o immagine
   |
   v
Ambiente di esecuzione
   |
   v
Applicazione in esecuzione
   |
   v
Osservabilità e feedback operativo
```

Questa mappa non è una sequenza rigida di UD.  
È una rappresentazione del flusso DevOps che useremo come riferimento.

---

# 3. Attività 1 - Assegna il ruolo corretto

Compila la tabella.

| Componente | Ruolo nel flusso DevOps cloud |
|---|---|
| GitHub |  |
| Azure DevOps Pipelines |  |
| Azure Container Registry |  |
| Azure Container Instances |  |
| Azure Container Apps |  |
| Application Insights |  |
| Azure Monitor |  |
| Log Analytics |  |

---

# 4. Attività 2 - Spiega il passaggio dal lavoro manuale al ciclo DevOps

Rispondi con 5-8 righe.

Domanda:

```text
Che differenza c'è tra creare o verificare risorse manualmente su Azure e inserirle in un ciclo DevOps automatizzato?
```

Scrivi qui la risposta:

```text
...
```

---

# 5. Attività 3 - Individua cosa appartiene alla UD11

Compila la tabella indicando se l'attività appartiene alla UD11.

| Attività | Appartiene alla UD11? | Motivo |
|---|---|---|
| Capire che cos'è DevOps |  |  |
| Distinguere CI e CD |  |  |
| Creare o verificare organizzazione Azure DevOps |  |  |
| Creare o verificare progetto Azure DevOps |  |  |
| Individuare la sezione Pipelines |  |  |
| Individuare la sezione Project settings |  |  |
| Individuare dove si creeranno le service connection |  |  |
| Costruire una immagine Docker locale |  |  |
| Fare push di una immagine su ACR |  |  |
| Eseguire un deploy automatico su Azure |  |  |
| Analizzare telemetria applicativa in Application Insights |  |  |

---

# 6. Attività 4 - Ricostruisci il flusso generale

Completa la mappa usando parole tue.

```text
Codice sorgente
   ->
...
   ->
Pipeline
   ->
...
   ->
Registry / artifact store
   ->
...
   ->
Ambiente di esecuzione
   ->
...
   ->
Osservabilità
   ->
...
```

Lo scopo non è indovinare una sequenza ufficiale, ma spiegare il senso del flusso.

---

# 7. Attività 5 - Errore concettuale

Leggi questa frase:

```text
GitHub, ACR e Azure DevOps sono più o meno la stessa cosa: servono tutti a mettere online l'applicazione.
```

Spiega perché è sbagliata.

Risposta:

```text
...
```

---

# 8. Consegna

Crea il file:

```bash
code docs/evidence_ud11_mappa_flusso.md
```

Inserisci:

- tabella Attività 1 compilata;
- risposta Attività 2;
- tabella Attività 3 compilata;
- mappa generale dell'Attività 4;
- correzione dell'errore concettuale.

---

# 9. Cosa devi saper dire a voce

Alla fine devi saper spiegare:

```text
Il codice vive in un repository.
La pipeline automatizza build, test, packaging e deploy.
Le immagini container vengono pubblicate in un registry.
Il deploy rende disponibile l'applicazione in un ambiente di esecuzione.
L'observability serve a capire come il sistema si comporta dopo il rilascio.
```

