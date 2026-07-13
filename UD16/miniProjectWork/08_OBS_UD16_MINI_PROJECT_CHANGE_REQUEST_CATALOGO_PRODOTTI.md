# OBS UD16 — Mini Project Work post-UD16

## Change urgente: rilascio del catalogo prodotti

### Scenario

Il cliente comunica una richiesta urgente: la nuova release dell'applicazione FE/BE integra un catalogo prodotti e deve essere pubblicata nell'Azure Container Registry già utilizzato, quindi rilasciata nelle Azure Container Apps create durante UD16.

Il codice sorgente è funzionante, ma è stato consegnato con documentazione minima. Prima del rilascio il team deve leggerlo in Visual Studio Code e aggiungere commenti tecnici utili alla manutenzione.

Non dobbiamo creare un nuovo ACR, un nuovo Container Apps Environment o nuove Container Apps. La change aggiorna le applicazioni già esistenti e produce nuove revisioni.

## Obiettivi

Al termine dell'attività dobbiamo saper:

1. prendere in carico e compilare una change request semplice;
2. leggere e documentare codice Python e Dockerfile in VS Code;
3. eseguire build e pubblicazione delle nuove immagini in ACR;
4. aggiornare prima il backend e poi il frontend in Azure Container Apps;
5. verificare che il catalogo prodotti sia raggiungibile.

## Materiale consegnato

```text
release-products/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
└── frontend/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    └── .dockerignore

azure-pipelines-ud16-change-products.yml
```

## 1. Compiliamo la change request

Creiamo nel repository il file:

```text
work/UD16/CHANGE_REQUEST_PRODUCTS.md
```

Usiamo questo modello essenziale:

```md
# Change Request — Catalogo prodotti

- Change ID: CHG-UD16-PRODUCTS-001
- Data:
- Richiedente: Cliente
- Descrizione: rilascio della nuova versione FE/BE con catalogo prodotti
- Componenti coinvolti: frontend, backend, ACR, Azure Container Apps
- Versione precedente:
- Nuova versione: generata dalla pipeline
- Impatto previsto: nuova revisione backend e nuova revisione frontend
- Piano di verifica: apertura della pagina, controllo health, ready e version
- Piano di rollback: riattivazione della revisione precedente
- Esito finale: DA COMPILARE DOPO IL RILASCIO
```

La change request deve descrivere con chiarezza che cosa cambiamo, quali componenti tocchiamo, come verifichiamo il risultato e come potremmo tornare alla versione precedente.

## 2. Apriamo e documentiamo il codice in VS Code

Apriamo la directory del repository con Visual Studio Code e analizziamo:

- `release-products/backend/app.py`;
- `release-products/frontend/app.py`;
- i due `Dockerfile`.

Aggiungiamo commenti nei punti importanti. Non dobbiamo commentare ogni istruzione.

I commenti devono spiegare almeno:

- configurazione tramite variabili d'ambiente;
- responsabilità del frontend e del backend;
- creazione e propagazione del `request_id`;
- produzione dei log JSON e calcolo della latenza;
- endpoint del catalogo normale, lento e di errore;
- uso di `BACKEND_URL` nel frontend;
- funzione dei passaggi principali dei Dockerfile.

Esempio utile:

```python
# URL del backend chiamato dal frontend. In Azure Container Apps
# deve indicare il FQDN interno del backend, non localhost.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

Esempio da evitare:

```python
# Legge BACKEND_URL.
BACKEND_URL = os.getenv("BACKEND_URL")
```

### Regola

Possiamo aggiungere commenti e docstring, ma non dobbiamo cambiare endpoint, porte, risposte JSON o comportamento applicativo.

### Verifica rapida

Dalla radice che contiene `release-products` eseguiamo:

```bash
python -m compileall release-products/backend release-products/frontend
```

## 3. Salviamo le modifiche nel repository

Controlliamo e pubblichiamo il codice commentato:

```bash
git status
git add work/UD16/release-products work/UD16/CHANGE_REQUEST_PRODUCTS.md
git commit -m "docs: commenta release catalogo prodotti"
git push
```

La pipeline usa il codice presente nel repository remoto. Un file modificato soltanto in locale non viene incluso nella build eseguita dall'agente Azure DevOps.

## 4. Configuriamo la pipeline della change

Copiamo il file:

```text
azure-pipelines-ud16-change-products.yml
```

nel repository, per esempio in:

```text
work/UD16/azure-pipelines-change-products.yml
```

Nel file valorizziamo soltanto le variabili che dipendono dal nostro ambiente:

```yaml
azureServiceConnection: 'sc-obs-azure-rg'
resourceGroupName: 'NOME_RESOURCE_GROUP'
acrName: 'NOME_ACR'
backendContainerAppName: 'NOME_ACA_BACKEND'
frontendContainerAppName: 'NOME_ACA_FRONTEND'
sourceRoot: 'work/UD16/release-products'
```

Non modifichiamo `imageTag`: la pipeline genera un tag univoco nel formato `1.1.<BuildId>`.

## 5. Eseguiamo la pipeline

La pipeline svolge queste operazioni:

```text
Validate
   ↓
BuildAndPush
   ├── backend:<tag>
   └── frontend:<tag>
   ↓
DeployBackend
   ↓
DeployFrontend
   ↓
Verify
```

La pipeline non crea l'ambiente ACA e non crea nuove Container Apps. Verifica che le risorse UD16 esistano, costruisce le immagini tramite ACR, aggiorna le due app e crea nuove revisioni.

Avviamo manualmente la pipeline da Azure DevOps e seguiamo gli stage.

## 6. Verifica pratica finale

Al termine dobbiamo controllare soltanto:

- stage della pipeline completati;
- pagina principale con il catalogo prodotti;
- `/health` restituisce HTTP 200;
- `/ready` restituisce HTTP 200;
- `/version` mostra la nuova versione;
- in ACR sono presenti i nuovi tag FE e BE;
- in ACA sono individuabili le nuove revisioni.

Non è richiesta una raccolta estesa di screenshot. È sufficiente mostrare al docente la pipeline conclusa, il codice commentato e l'applicazione funzionante.

## 7. Chiudiamo la change

Aggiorniamo `CHANGE_REQUEST_PRODUCTS.md` indicando:

```text
- Versione precedente: <valore rilevato>
- Nuova versione: 1.1.<BuildId>
- Esito finale: SUCCESS / FAILED
- Nota finale: <eventuale problema e correzione>
```

Eseguiamo infine commit e push della change chiusa.

## Criteri di completamento

```text
[ ] Change request compilata.
[ ] Codice frontend e backend commentato in modo utile.
[ ] Dockerfile documentati nei passaggi principali.
[ ] Codice verificato con compileall.
[ ] Modifiche pubblicate nel repository.
[ ] Nuove immagini presenti in ACR.
[ ] Backend e frontend aggiornati in ACA.
[ ] Catalogo prodotti visibile.
[ ] Change request chiusa con l'esito finale.
```
