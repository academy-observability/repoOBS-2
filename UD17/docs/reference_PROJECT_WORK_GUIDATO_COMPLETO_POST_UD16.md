# Mini Project Work post-UD16 — Change request e rilascio guidato FE/BE

## Obiettivo

In questa attività prendiamo in carico una richiesta urgente del cliente e rilasciamo una nuova versione dell’applicazione composta da:

- **backend Flask**, che espone il catalogo prodotti;
- **frontend Flask**, che richiama il backend e visualizza i prodotti;
- due nuove immagini Docker;
- due repository distinti in Azure Container Registry;
- due nuove revisioni delle Container Apps già create in UD16new.

L’attività è completamente guidata. Non dobbiamo creare nuove risorse Azure: utilizziamo quelle già funzionanti al termine di UD16new.

---

# 1. Scenario della change request

Il cliente richiede il rilascio urgente della nuova versione dell’applicazione che integra il catalogo prodotti.

La nuova release deve:

1. essere documentata nel codice sorgente con commenti tecnici essenziali;
2. produrre due immagini distinte, frontend e backend;
3. pubblicare le immagini nell’ACR già esistente;
4. aggiornare il backend già distribuito in Azure Container Apps;
5. aggiornare il frontend già distribuito in Azure Container Apps;
6. verificare che il frontend raggiunga il backend e mostri il catalogo;
7. lasciare disponibili le revisioni precedenti per un eventuale rollback.

Non dobbiamo:

- creare un nuovo Resource Group;
- creare un nuovo ACR;
- creare un nuovo Container Apps Environment;
- creare nuove Container Apps;
- modificare il contratto applicativo;
- utilizzare `az acr build`;
- utilizzare il tag `latest`.

---

# 2. Risultato finale atteso

Al termine dobbiamo ottenere:

```text
Azure Container Registry
├── obsapp-products-backend:<BuildId>
└── obsapp-products-frontend:<BuildId>

Azure Container Apps Environment esistente
├── Container App backend
│   └── nuova revisione con obsapp-products-backend:<BuildId>
└── Container App frontend
    └── nuova revisione con obsapp-products-frontend:<BuildId>
```

Il frontend deve essere raggiungibile pubblicamente.

Il backend deve mantenere ingress interno.

Il flusso applicativo deve essere:

```text
Browser
   ↓
Frontend ACA
   ↓  BACKEND_URL
Backend ACA
   ↓
Catalogo prodotti
```

---

# 3. Prerequisiti

Prima di iniziare verifichiamo di avere già completato UD16new.

Devono esistere:

```text
[ ] Resource Group
[ ] Azure Container Registry
[ ] Container Apps Environment
[ ] Container App backend
[ ] Container App frontend
[ ] Service connection Azure DevOps funzionante
[ ] Repository Git aggiornato
```

Il backend e il frontend devono appartenere allo stesso Container Apps Environment.

## 3.1 Dati da annotare

Compiliamo questa tabella prima di modificare la pipeline:

| Dato | Valore reale |
|---|---|
| Nome service connection Azure DevOps | |
| Resource Group | |
| Azure Container Registry | |
| Container App backend | |
| Container App frontend | |
| Branch Git | `main` |
| Percorso sorgenti prodotti | `work/UD16/release-products` |

## 3.2 Come trovare i nomi delle risorse dal portale

### Resource Group

```text
Azure Portal
→ Resource groups
→ aprire il gruppo utilizzato in UD16new
```

### Azure Container Registry

```text
Azure Portal
→ Container registries
→ aprire il registry utilizzato in UD15/UD16
```

Annotiamo il **nome della risorsa**, non il login server completo.

Esempio:

```text
acrobsud13ep
```

Non inseriamo:

```text
acrobsud13ep.azurecr.io
```

### Container Apps

```text
Azure Portal
→ Container Apps
→ individuare frontend e backend creati in UD16new
```

### Service connection

```text
Azure DevOps
→ Project settings
→ Service connections
→ aprire la connessione Azure usata nelle pipeline precedenti
```

Annotiamo esattamente il nome visualizzato.

---

# 4. Preparazione del progetto nel repository

Nel repository del corso dobbiamo ottenere questa struttura:

```text
work/UD16/
├── release-products/
│   ├── backend/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── .dockerignore
│   └── frontend/
│       ├── app.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── .dockerignore
├── 01_CHANGE_REQUEST.md
└── azure-pipelines-products.yml
```

Se il materiale ricevuto si trova in una cartella esterna, copiamo `release-products` dentro:

```text
work/UD16/
```

Da terminale, posizionati nella radice del repository:

```bash
pwd
ls
```

Verifichiamo i file:

```bash
find work/UD16/release-products -maxdepth 2 -type f | sort
```

Devono comparire almeno:

```text
work/UD16/release-products/backend/app.py
work/UD16/release-products/backend/Dockerfile
work/UD16/release-products/backend/requirements.txt
work/UD16/release-products/frontend/app.py
work/UD16/release-products/frontend/Dockerfile
work/UD16/release-products/frontend/requirements.txt
```

---

# 5. Compilazione della change request

Creiamo il file:

```text
work/UD16/01_CHANGE_REQUEST.md
```

Inseriamo questo contenuto e completiamo i valori mancanti:

```markdown
# Change Request — Catalogo prodotti

## Identificazione

- Change ID: CHG-UD16-PRODUCTS-001
- Richiedente: Cliente
- Esecutore: nome e cognome del partecipante
- Data: data corrente

## Descrizione

Rilascio della nuova versione frontend/backend che integra il catalogo prodotti.

## Componenti coinvolti

- repository Git del corso;
- immagine Docker backend;
- immagine Docker frontend;
- Azure Container Registry;
- Container App backend;
- Container App frontend.

## Impatto previsto

Le Container Apps esistenti verranno aggiornate con nuove immagini. Azure Container Apps creerà nuove revisioni applicative.

## Rischio principale

Il frontend potrebbe non raggiungere il backend se BACKEND_URL, ingress o porta non sono configurati correttamente.

## Piano di verifica

- controllo immagini e tag in ACR;
- controllo nuova revisione backend;
- controllo nuova revisione frontend;
- verifica /health;
- verifica /ready;
- verifica /version;
- verifica /products;
- apertura della home del frontend.

## Piano di rollback

Riattivazione della revisione precedente delle Container Apps qualora la nuova release non superi i test.

## Esito finale

- Stato: DA COMPLETARE
- Tag rilasciato: DA COMPLETARE
- Problemi riscontrati: DA COMPLETARE
- Correzioni effettuate: DA COMPLETARE
```

Per ora lasciamo la sezione **Esito finale** incompleta.

---

# 6. Apertura del codice in Visual Studio Code

Apriamo la radice del repository in VS Code tramite WSL.

Da terminale:

```bash
code .
```

Nell’Explorer apriamo:

```text
work
└── UD16
    └── release-products
        ├── backend
        │   └── app.py
        └── frontend
            └── app.py
```

---

# 7. Documentazione essenziale del codice sorgente

Non dobbiamo commentare ogni riga. Aggiungiamo commenti che spieghino responsabilità, configurazione e comportamento.

## 7.1 Backend

Nel file:

```text
work/UD16/release-products/backend/app.py
```

aggiungiamo commenti nei punti che descrivono:

- ruolo generale del backend;
- variabili d’ambiente;
- catalogo prodotti;
- generazione o propagazione del `request_id`;
- misurazione della latenza;
- log strutturati;
- endpoint normale;
- endpoint lento;
- endpoint di errore;
- health e version.

Esempio di commento adeguato:

```python
# Identifica il servizio nei log e consente di distinguere gli eventi
# prodotti dal backend da quelli prodotti dal frontend.
SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
```

Esempio da evitare:

```python
# Legge SERVICE_NAME
SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
```

## 7.2 Frontend

Nel file:

```text
work/UD16/release-products/frontend/app.py
```

aggiungiamo commenti nei punti che descrivono:

- ruolo generale del frontend;
- significato di `BACKEND_URL`;
- chiamata HTTP dal frontend al backend;
- propagazione del `request_id`;
- rendering della pagina;
- endpoint `/health`;
- endpoint `/ready`;
- endpoint `/products`;
- gestione di timeout ed errori backend.

Esempio:

```python
# URL utilizzato dal frontend per raggiungere il backend.
# In Azure Container Apps deve contenere il FQDN interno del backend
# e non localhost, perché FE e BE sono eseguiti in risorse distinte.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

## 7.3 Dockerfile

Apriamo:

```text
backend/Dockerfile
frontend/Dockerfile
```

Aggiungiamo brevi commenti che spieghino:

- immagine base;
- directory di lavoro;
- installazione delle dipendenze;
- copia del codice;
- porta esposta;
- comando di avvio.

Non modifichiamo le istruzioni Docker già presenti.

---

# 8. Verifica sintattica del codice

Dalla radice del repository eseguiamo:

```bash
python3 -m compileall -q \
  work/UD16/release-products/backend \
  work/UD16/release-products/frontend
```

Se il comando non mostra errori, la sintassi Python è valida.

Controlliamo lo stato Git:

```bash
git status
```

Dovremmo vedere modifiche nei file commentati e nel file della change request.

---

# 9. Preparazione della pipeline completa

Copiamo il file docente completo:

```text
azure-pipelines-products-SVOLGIMENTO-COMPLETO-v4.yml
```

nel repository con il nome:

```text
work/UD16/azure-pipelines-products.yml
```

La pipeline utilizza intenzionalmente:

```text
az acr login
Docker build
Docker push
az containerapp update
```

Non utilizza:

```text
az acr build
```

Questo evita la dipendenza da ACR Tasks.

---

# 10. Valorizzazione delle variabili YAML

Apriamo:

```text
work/UD16/azure-pipelines-products.yml
```

All’inizio troviamo:

```yaml
variables:
  azureServiceConnection: 'NOME_SERVICE_CONNECTION'
  resourceGroupName: 'NOME_RESOURCE_GROUP'
  acrName: 'NOME_ACR'
  backendContainerAppName: 'NOME_ACA_BACKEND'
  frontendContainerAppName: 'NOME_ACA_FRONTEND'

  backendRepository: 'obsapp-products-backend'
  frontendRepository: 'obsapp-products-frontend'

  backendPort: '8000'
  frontendPort: '8000'

  sourceRoot: 'work/UD16/release-products'

  imageTag: '$(Build.BuildId)'
```

Sostituiamo solamente i valori segnaposto.

Esempio:

```yaml
variables:
  azureServiceConnection: 'sc-obs-azure'
  resourceGroupName: 'rg-obs-ud05-gpastore'
  acrName: 'acrobsud13gpastore'
  backendContainerAppName: 'ca-obs-ud16-backend'
  frontendContainerAppName: 'ca-obs-ud16-frontend'

  backendRepository: 'obsapp-products-backend'
  frontendRepository: 'obsapp-products-frontend'

  backendPort: '8000'
  frontendPort: '8000'

  sourceRoot: 'work/UD16/release-products'

  imageTag: '$(Build.BuildId)'
```

L’esempio deve essere sostituito con i nomi reali del partecipante.

## 10.1 Significato di `imageTag`

La pipeline usa:

```yaml
imageTag: '$(Build.BuildId)'
```

Azure DevOps sostituisce `$(Build.BuildId)` con il numero reale del run.

Se il Build ID è `145`, verranno pubblicate:

```text
obsapp-products-backend:145
obsapp-products-frontend:145
```

Il tag può essere uguale perché i repository sono differenti.

---

# 11. Controllo della pipeline prima del push

Verifichiamo che non siano rimasti segnaposto:

```bash
grep -nE 'NOME_|INSERIRE_' work/UD16/azure-pipelines-products.yml
```

Il comando non deve restituire righe relative alle variabili da compilare.

Verifichiamo il percorso sorgenti:

```bash
test -f work/UD16/release-products/backend/Dockerfile && echo "Backend Dockerfile OK"
test -f work/UD16/release-products/frontend/Dockerfile && echo "Frontend Dockerfile OK"
```

Risultato atteso:

```text
Backend Dockerfile OK
Frontend Dockerfile OK
```

---

# 12. Commit e push

Controlliamo le modifiche:

```bash
git status
```

Aggiungiamo i file:

```bash
git add work/UD16
```

Creiamo il commit:

```bash
git commit -m "UD16 - change request catalogo prodotti e pipeline release"
```

Invio al repository remoto:

```bash
git push
```

Controlliamo:

```bash
git status
```

Risultato atteso:

```text
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

# 13. Creazione della pipeline in Azure DevOps

La pipeline contiene:

```yaml
trigger: none
pr: none
```

Questo significa che il push non avvia automaticamente il run. L’avvio sarà manuale.

Nel portale Azure DevOps:

```text
Pipelines
→ New pipeline
→ GitHub
→ selezionare il repository del partecipante
→ Existing Azure Pipelines YAML file
```

Selezioniamo:

```text
Branch: main
Path: /work/UD16/azure-pipelines-products.yml
```

Confermiamo con:

```text
Continue
→ Save
```

Assegniamo un nome riconoscibile, per esempio:

```text
Mini Project Work post-UD16 - Products Release
```

---

# 14. Avvio manuale della pipeline

Apriamo la pipeline:

```text
Pipelines
→ Mini Project Work post-UD16 - Products Release
→ Run pipeline
```

Controlliamo:

```text
Branch/tag: main
```

Avviamo con:

```text
Run
```

---

# 15. Lettura degli stage

La pipeline è composta da quattro stage:

```text
1 - Validate prerequisites
        ↓
2 - Build and push product images to ACR
        ↓
3 - Update backend ACA revision
        ↓
4 - Update frontend ACA revision and verify
```

Ogni stage parte solo se il precedente termina con successo.

---

# 16. Stage 1 — Validate prerequisites

Questo stage controlla:

- variabili compilate;
- presenza dei Dockerfile;
- presenza dei file `app.py`;
- sintassi Python;
- disponibilità di Docker sull’agente;
- esistenza del Resource Group;
- esistenza dell’ACR;
- esistenza delle due Container Apps;
- appartenenza di FE e BE allo stesso environment.

Risultato atteso:

```text
Prerequisiti verificati.
Source root: .../work/UD16/release-products
Tag della release: <BuildId>
```

Se questo stage fallisce, non passiamo alla build. Correggiamo il valore indicato nel messaggio di errore.

---

# 17. Stage 2 — Build and push in ACR

La pipeline:

1. recupera il login server dell’ACR;
2. esegue il login;
3. costruisce l’immagine backend;
4. esegue il push backend;
5. costruisce l’immagine frontend;
6. esegue il push frontend;
7. mostra gli ultimi tag presenti nei due repository.

Nel log dobbiamo trovare righe simili a:

```text
Backend image: <acr>.azurecr.io/obsapp-products-backend:<BuildId>
Frontend image: <acr>.azurecr.io/obsapp-products-frontend:<BuildId>
```

Al termine devono comparire i nuovi tag.

## 17.1 Verifica dal portale

```text
Azure Portal
→ Container Registry
→ Repositories
```

Devono esistere:

```text
obsapp-products-backend
obsapp-products-frontend
```

Apriamo entrambi e verifichiamo che contengano il Build ID del run.

---

# 18. Stage 3 — Deploy backend

La pipeline aggiorna prima il backend perché il nuovo frontend dipende dai nuovi endpoint prodotti.

Operazioni eseguite:

```text
Ingress backend → internal
Target port → 8000
Immagine → obsapp-products-backend:<BuildId>
APP_ENV → aca
SERVICE_NAME → backend
APP_VERSION → <BuildId>
PORT → 8000
```

Al termine la pipeline mostra le revisioni backend.

## 18.1 Verifica dal portale

```text
Azure Portal
→ Container Apps
→ backend
→ Revision management
```

Verifichiamo:

- presenza di una nuova revisione;
- immagine `obsapp-products-backend:<BuildId>`;
- stato attivo/sano;
- ingress interno.

Non cancelliamo la revisione precedente.

---

# 19. Stage 4 — Deploy frontend e smoke test

La pipeline:

1. recupera il FQDN interno del backend;
2. costruisce `BACKEND_URL`;
3. mantiene il frontend con ingress esterno;
4. aggiorna l’immagine frontend;
5. imposta le variabili d’ambiente;
6. recupera il FQDN pubblico del frontend;
7. attende la disponibilità della nuova revisione;
8. esegue gli smoke test.

Configurazione attesa:

```text
Ingress frontend → external
Target port → 8000
Immagine → obsapp-products-frontend:<BuildId>
APP_ENV → aca
SERVICE_NAME → frontend
APP_VERSION → <BuildId>
PORT → 8000
BACKEND_URL → https://<fqdn-interno-backend>
```

La pipeline verifica:

```text
/health
/ready
/version
/products
/
```

Risultato finale atteso:

```text
Smoke test completati con successo.
```

---

# 20. Verifica manuale dell’applicazione

Nel portale:

```text
Azure Portal
→ Container Apps
→ frontend
→ Overview
→ Application Url
```

Apriamo l’URL nel browser.

Dobbiamo visualizzare la pagina:

```text
Catalogo prodotti
```

Verifichiamo anche gli endpoint, sostituendo `<FRONTEND_URL>`:

```bash
curl -i "<FRONTEND_URL>/health"
curl -i "<FRONTEND_URL>/ready"
curl -i "<FRONTEND_URL>/version"
curl -i "<FRONTEND_URL>/products"
```

Risultati attesi:

```text
/health   → HTTP 200
/ready    → HTTP 200 e backend_status 200
/version  → contiene il Build ID
/products → contiene il catalogo
```

La home:

```text
<FRONTEND_URL>/
```

deve visualizzare il catalogo in HTML.

---

# 21. Chiusura della change request

Torniamo al file:

```text
work/UD16/01_CHANGE_REQUEST.md
```

Completiamo:

```markdown
## Esito finale

- Stato: SUCCESS
- Tag rilasciato: <BuildId>
- Problemi riscontrati: descrivere brevemente oppure scrivere Nessuno
- Correzioni effettuate: descrivere brevemente oppure scrivere Non necessarie
```

Esempio:

```markdown
## Esito finale

- Stato: SUCCESS
- Tag rilasciato: 145
- Problemi riscontrati: percorso sourceRoot inizialmente errato
- Correzioni effettuate: corretto il percorso in work/UD16/release-products
```

Eseguiamo il commit finale:

```bash
git add work/UD16/01_CHANGE_REQUEST.md
git commit -m "UD16 - chiusura change request catalogo prodotti"
git push
```

---

# 22. Checklist finale

```text
[ ] Ho compilato la change request.
[ ] Ho aperto FE e BE in VS Code.
[ ] Ho aggiunto commenti tecnici essenziali.
[ ] La sintassi Python è valida.
[ ] Ho valorizzato le variabili reali della pipeline.
[ ] Ho eseguito commit e push.
[ ] Ho creato la pipeline dal file YAML corretto.
[ ] Lo stage Validate è riuscito.
[ ] Le due immagini sono presenti in repository ACR distinti.
[ ] Il backend è stato aggiornato prima del frontend.
[ ] Il backend mantiene ingress interno.
[ ] Il frontend mantiene ingress esterno.
[ ] BACKEND_URL contiene il FQDN backend e non localhost.
[ ] /health restituisce 200.
[ ] /ready restituisce 200.
[ ] /version mostra il Build ID corretto.
[ ] /products restituisce il catalogo.
[ ] La home mostra il catalogo prodotti.
[ ] Le revisioni precedenti non sono state eliminate.
[ ] Ho completato l’esito finale della change request.
```

---

# 23. Troubleshooting rapido

## 23.1 Il push Git non avvia la pipeline

È normale perché il file contiene:

```yaml
trigger: none
```

Avviamo manualmente:

```text
Pipelines → selezionare pipeline → Run pipeline
```

## 23.2 `Dockerfile backend non trovato`

Controlliamo:

```yaml
sourceRoot: 'work/UD16/release-products'
```

E verifichiamo:

```bash
ls -l work/UD16/release-products/backend/Dockerfile
```

## 23.3 `TasksOperationsNotAllowed`

Significa che è stata utilizzata una vecchia pipeline contenente:

```bash
az acr build
```

La pipeline corretta deve usare:

```text
az acr login
Docker build
Docker push
```

## 23.4 `unauthorized` o `denied` durante `docker push`

La service connection riesce ad autenticarsi ad Azure ma non dispone dell’autorizzazione a pubblicare nell’ACR.

Informiamo il docente. Deve essere verificato il ruolo di push assegnato all’identità della service connection sul registry.

## 23.5 Il backend deploya, ma `/ready` restituisce 503

Controlliamo nel frontend:

```text
BACKEND_URL
```

Non deve contenere:

```text
localhost
```

Deve contenere:

```text
https://<fqdn-interno-backend>
```

Controlliamo inoltre:

- backend in stato Running;
- ingress backend interno;
- target port 8000;
- FE e BE nello stesso Container Apps Environment.

## 23.6 Lo smoke test restituisce 404 sulla home

Verifichiamo che il frontend utilizzi realmente l’immagine:

```text
obsapp-products-frontend:<BuildId>
```

La versione products espone la route:

```text
/
```

Una vecchia immagine UD16new potrebbe esporre solamente `/demo`.

## 23.7 La nuova revisione non è immediatamente disponibile

La pipeline attende e ripete gli smoke test. Non interrompiamo al primo tentativo fallito.

Se il timeout viene superato, apriamo:

```text
Container App → Revision management
Container App → Log stream
```

Verifichiamo:

- stato della nuova revisione;
- errori di avvio;
- immagine configurata;
- variabili d’ambiente;
- porta configurata.

## 23.8 La pipeline aggiorna la risorsa sbagliata

Controlliamo con attenzione:

```yaml
backendContainerAppName
frontendContainerAppName
resourceGroupName
```

I nomi devono corrispondere alle risorse create dal singolo partecipante in UD16new.

---

# 24. Conclusione

Con questa attività abbiamo eseguito un flusso completo di change e release:

```text
Richiesta del cliente
        ↓
Analisi e documentazione del codice
        ↓
Build automatica FE/BE
        ↓
Push in ACR
        ↓
Aggiornamento backend ACA
        ↓
Aggiornamento frontend ACA
        ↓
Smoke test
        ↓
Chiusura della change request
```

Il risultato non è soltanto un’applicazione funzionante: è una release tracciabile, ripetibile e verificata tramite pipeline.
