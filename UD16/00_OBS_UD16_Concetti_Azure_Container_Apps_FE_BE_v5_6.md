# UD16 - Concetti
## Deploy FE/BE su Azure Container Apps

## 1. Perché UD16

Nelle UD precedenti abbiamo fatto tre passaggi:

```text
UD12 = Docker locale su app singola
UD13 = primo deploy automatico app singola su ACR/ACI
UD14 = pipeline multistage app singola con smoke test
UD15 = FE/BE locale + due immagini + push su ACR
```

UD16 porta il sistema FE/BE in cloud.

Il punto centrale non è più costruire l'immagine. Il punto centrale è:

```text
prendere immagini già pubblicate in ACR
-> eseguirle come servizi cloud separati
-> configurare la relazione frontend -> backend
-> verificare revisioni, log e stato runtime
```

## 2. Che cos'è Azure Container Apps

Azure Container Apps è un servizio Azure per eseguire applicazioni containerizzate senza gestire direttamente VM, orchestratori o nodi Kubernetes.

Nel nostro laboratorio lo usiamo per creare:

```text
backend Container App
frontend Container App
```

Ogni Container App esegue una immagine Docker proveniente da ACR.

## 3. Concetti essenziali

| Concetto | Significato nel laboratorio |
|---|---|
| ACR | Registry dove sono salvate le immagini `backend` e `frontend` |
| ACA Environment | Ambiente logico che contiene le Container Apps |
| Container App | Servizio applicativo containerizzato |
| Ingress | Regola che espone HTTP/HTTPS verso la Container App |
| Target port | Porta interna su cui ascolta il container |
| FQDN | URL assegnato da ACA alla Container App |
| Revisione | Versione runtime generata quando cambia immagine o configurazione |

## 4. Differenza con ACI

ACI, usato in UD13 e UD14, era utile per il primo deploy semplice.

ACA è più adatto a sistemi applicativi composti da più servizi perché introduce:

- revisioni;
- ingress gestito;
- scaling;
- ambiente comune;
- integrazione migliore con log e osservabilità cloud.

## 5. Il punto didattico di BACKEND_URL

Il frontend non deve conoscere il backend in modo rigido nel codice.

Il frontend riceve:

```text
BACKEND_URL=https://<backend-fqdn>
```

Questa configurazione viene passata dalla pipeline durante il deploy del frontend.

## 6. Pipeline UD16

La pipeline UD16 non fa build delle immagini. Usa le immagini già esistenti.

Stage previsti:

```text
ValidateInputs
DeployEnvironment
DeployBackend
DeployFrontend
VerifyDeploy
```

Questa separazione serve a rendere chiaro dove si rompe il processo.

## 7. Messaggio chiave

> In UD15 abbiamo prodotto gli artefatti container. In UD16 li eseguiamo come servizi cloud separati, configurando la relazione frontend/backend e verificando che il runtime funzioni davvero.
