# UD14 - Concetti
## Pipeline multistage, rilascio verificabile e smoke test

---

# 1. Scopo della UD14

Nella UD13 abbiamo costruito un primo flusso automatico completo:

```text
GitHub -> Azure DevOps Pipeline -> ACR -> ACI -> verifica manuale
```

Quel flusso dimostra che il deploy automatico è possibile. La UD14 serve a migliorare la qualità del processo.

Una pipeline che arriva in fondo non è automaticamente una buona pipeline. Una pipeline utile deve far capire:

- quale fase sta eseguendo;
- dove si è verificato un errore;
- quale immagine è stata prodotta;
- quale versione è stata distribuita;
- se l'applicazione risponde davvero dopo il deploy.

Per questo trasformiamo la pipeline compatta della UD13 in una pipeline multistage.

---

# 2. Obiettivo della UD14

Alla fine dell'attività dobbiamo essere in grado di spiegare e mostrare questo flusso:

```text
ValidateRepository
  -> BuildAndPush
  -> DeployToACI
  -> SmokeTest
```

Il punto centrale è questo:

```text
Non basta distribuire un container.
Bisogna verificare automaticamente che il servizio distribuito risponda agli endpoint essenziali.
```

---

# 3. Pipeline monolitica e pipeline multistage

## 3.1 Pipeline monolitica

Una pipeline monolitica mette tutte le operazioni in un unico blocco:

```text
checkout
build
push
deploy
verifica
```

Funziona, ma ha un limite: se qualcosa fallisce, la lettura del problema è meno immediata.

## 3.2 Pipeline multistage

Una pipeline multistage divide il processo in fasi logiche:

| Stage | Responsabilità |
|---|---|
| `ValidateRepository` | verifica struttura e sintassi minima |
| `BuildAndPush` | costruisce l'immagine e la pubblica in ACR |
| `DeployToACI` | crea o aggiorna il container in Azure Container Instances |
| `SmokeTest` | verifica che l'applicazione risponda davvero |

Questa divisione rende il rilascio più leggibile e più diagnosticabile.

---

# 4. Stage, job e step

In Azure Pipelines useremo questi concetti:

| Concetto | Significato pratico |
|---|---|
| Pipeline | intero processo automatico |
| Stage | fase logica del processo |
| Job | gruppo di operazioni eseguite da un agente |
| Step | singolo comando o task |

Per questa UD non serve ancora usare ambienti approvati, controlli manuali o governance avanzata. Ci concentriamo sulla struttura minima leggibile.

---

# 5. Perché lo smoke test è importante

Il deploy può riuscire tecnicamente anche se l'applicazione non è realmente utilizzabile.

Esempi:

- il container è stato creato ma l'app non è ancora pronta;
- la porta è sbagliata;
- l'app si avvia ma restituisce errore;
- il FQDN esiste ma l'endpoint `/health` non risponde.

Lo smoke test serve a verificare gli endpoint essenziali dopo il deploy.

Nella UD14 testeremo:

```text
GET /
GET /health
GET /time
POST /echo
```

Non useremo `/error` nello smoke test bloccante perché quell'endpoint restituisce volutamente un errore `500`. Sarà usato solo nei test manuali e nelle evidenze.

---

# 6. Tag immagine e Build ID

La pipeline userà `$(Build.BuildId)` come tag dell'immagine.

Esempio:

```text
nomeacr.azurecr.io/obsapp-ud14:152
```

Il valore `152` identifica il run della pipeline.

Questo aiuta a collegare:

```text
run pipeline -> tag immagine -> container distribuito -> risposta applicativa
```

È molto più chiaro rispetto a usare sempre `latest`.

---

# 7. Differenza tra build riuscita, deploy riuscito e app funzionante

Questi tre risultati non sono equivalenti.

| Stato | Significato |
|---|---|
| Build riuscita | l'immagine è stata costruita |
| Push riuscito | l'immagine è arrivata in ACR |
| Deploy riuscito | ACI è stato creato o aggiornato |
| Smoke test riuscito | l'applicazione risponde agli endpoint essenziali |

La pipeline UD14 sarà considerata realmente riuscita solo dopo lo smoke test.

---

# 8. Cosa resta una semplificazione da laboratorio

In questa UD useremo ancora alcune semplificazioni:

- ACI come target cloud semplice;
- account admin ACR abilitato;
- cancellazione e ricreazione del container ACI;
- nessuna approvazione manuale;
- nessun ambiente staging/prod.

Queste scelte servono a mantenere il laboratorio leggibile. Non sono una ricetta completa per ambienti di produzione.

---

# 9. Mappa mentale finale

```text
Repository GitHub
  -> Pipeline Azure DevOps
      -> ValidateRepository
      -> BuildAndPush
          -> ACR
      -> DeployToACI
          -> ACI
      -> SmokeTest
          -> HTTP endpoint checks
      -> Logs
```

La UD14 aggiunge qualità al rilascio: non cambia l'applicazione, migliora il processo.
