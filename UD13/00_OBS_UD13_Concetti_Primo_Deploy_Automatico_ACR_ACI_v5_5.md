# UD13 - Concetti
## Primo deploy automatico cloud con GitHub, Azure DevOps, ACR e ACI

---

# 1. Scopo della UD13

Questa UD introduce il primo flusso DevOps cloud completo su una singola applicazione containerizzata.

Nella UD precedente abbiamo imparato a costruire ed eseguire un container in locale. Ora spostiamo il ragionamento dentro un flusso automatizzato:

```text
GitHub
  -> Azure DevOps Pipeline
  -> Docker build su agent
  -> Azure Container Registry
  -> Azure Container Instances
  -> verifica HTTP
  -> log cloud
```

La differenza non è solo tecnica. È metodologica: il deploy non dipende più da una sequenza manuale eseguita sul PC del partecipante, ma da una procedura dichiarata, tracciabile e ripetibile.

---

# 2. Dal Docker locale al Docker nella pipeline

| UD12 | UD13 |
|---|---|
| `docker build` eseguito dal partecipante | `docker build` eseguito dall'agent Azure DevOps |
| immagine Docker locale | immagine pubblicata su ACR |
| container eseguito sul PC | container eseguito su ACI |
| test su `localhost` | test su FQDN pubblico Azure |
| `docker logs` | `az container logs` |

Il principio è lo stesso: una immagine contiene applicazione, runtime e dipendenze. Cambia il luogo in cui questa immagine viene costruita, conservata ed eseguita.

---

# 3. Ruolo di GitHub

GitHub resta il repository del codice.

Nel repository ci saranno:

- codice dell'applicazione;
- `requirements.txt`;
- `Dockerfile`;
- `.dockerignore`;
- file `azure-pipelines.yml`;
- documentazione ed evidenze.

GitHub non è il registry immagini e non è il target di deploy. In questa UD è la sorgente da cui parte la pipeline.

---

# 4. Ruolo di Azure DevOps

Azure DevOps viene usato per Azure Pipelines.

La pipeline esegue automaticamente:

1. checkout del repository GitHub;
2. login verso Azure tramite service connection;
3. login verso ACR;
4. build dell'immagine Docker;
5. push dell'immagine nel registry;
6. creazione o sostituzione del container ACI;
7. stampa del FQDN finale.

La pipeline trasforma una modifica versionata nel repository in un deployment verificabile.

---

# 5. Ruolo di Azure Container Registry

Azure Container Registry, abbreviato ACR, è il registry immagini.

Il codice non viene deployato direttamente. La pipeline costruisce una immagine e la pubblica in ACR con un nome del tipo:

```text
nomeacr.azurecr.io/obsapp-ud13:TAG
```

Il tag usato nella UD è collegato al run della pipeline tramite `Build.BuildId`. Questo aiuta a collegare:

```text
run pipeline -> tag immagine -> container deployato
```

---

# 6. Ruolo di Azure Container Instances

Azure Container Instances, abbreviato ACI, è il primo target cloud semplice.

ACI consente di eseguire un container nel cloud senza introdurre una piattaforma più complessa. In questa UD serve a capire il deploy automatico di una singola applicazione.

ACI espone:

- un nome container;
- un FQDN pubblico;
- una o più porte;
- log del processo eseguito nel container.

---

# 7. Service connection

La pipeline deve potersi autenticare verso Azure. Per questo si usa una Azure Resource Manager service connection.

Nel laboratorio la service connection avrà un nome chiaro, ad esempio:

```text
sc-obs-azure-rg
```

Il nome viene richiamato nel file YAML:

```yaml
azureServiceConnection: 'sc-obs-azure-rg'
```

Se il nome nel portale e quello nel file YAML non coincidono, la pipeline fallisce.

---

# 8. Semplificazione didattica su ACR admin

Per rendere il primo deploy più lineare, il laboratorio abilita l'admin account di ACR e usa le credenziali del registry per permettere ad ACI di scaricare l'immagine.

Questo va considerato una semplificazione da aula.

In scenari più maturi si preferiscono approcci come managed identity, service principal o workload identity federation. In questa UD non li implementiamo per non sovraccaricare il primo ciclo automatico.

---

# 9. Cosa deve saper spiegare il partecipante

Alla fine della UD il partecipante deve saper rispondere a queste domande:

- Dove vive il codice?
- Dove gira la pipeline?
- Dove viene costruita l'immagine?
- Dove viene salvata l'immagine?
- Dove gira il container finale?
- Come verifico il FQDN del container?
- Come leggo i log cloud?
- Quale differenza c'è tra `docker logs` e `az container logs`?
- Perché il deploy automatico è più ripetibile di una procedura manuale?

---

# 10. Mappa minima da ricordare

```text
Codice
  -> GitHub
  -> Azure DevOps Pipeline
  -> docker build
  -> ACR
  -> ACI
  -> curl
  -> az container logs
```

Questa è la mappa tecnica della UD13.
