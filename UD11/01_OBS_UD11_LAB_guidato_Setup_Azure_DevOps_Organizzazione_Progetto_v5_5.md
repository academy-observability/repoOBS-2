# OBS UD11 - Laboratorio guidato
## Setup Azure DevOps: organizzazione, progetto e prerequisiti per le pipeline

Versione: v5.5  
Destinatari: partecipanti  
Durata consigliata: 2 ore  
Tipo attività: laboratorio guidato senza Docker operativo

---

# 1. Obiettivo del laboratorio

In questo laboratorio prepariamo l'ambiente Azure DevOps che useremo nelle UD successive.

Alla fine dovrai avere:

- accesso a una organizzazione Azure DevOps;
- un progetto Azure DevOps dedicato al percorso Observability/DevOps;
- accesso alla sezione Pipelines;
- accesso alla sezione Project settings;
- consapevolezza di dove saranno create le service connection;
- un file di evidenza che documenta l'ambiente creato.

In questo laboratorio non creiamo ancora pipeline operative e non facciamo deploy.

---

# 2. Prima di iniziare

Per completare il laboratorio devi avere almeno uno di questi account:

- account Microsoft personale;
- account aziendale o scolastico;
- account GitHub utilizzabile per autenticarti o collegare repository.

Nel percorso useremo:

```text
GitHub = repository del codice
Azure DevOps = motore CI/CD
Azure = piattaforma di deploy
```

Per questo oggi prepariamo solo il contenitore Azure DevOps.

---

# 3. Convenzioni di naming consigliate

Usiamo nomi semplici e riconoscibili.

## 3.1 Organizzazione Azure DevOps

Esempi:

```text
academy-observability-nomecognome
corso-observability-nome
observability-devops-nome
```

## 3.2 Progetto Azure DevOps

Nome consigliato:

```text
Observability-DevOps
```

## 3.3 Perché i nomi contano

Nelle prossime UD dovremo riconoscere rapidamente:

- organizzazione;
- progetto;
- pipeline;
- service connection;
- repository collegati;
- risorse Azure usate.

Nomi casuali rendono il troubleshooting più lento.

---

# 4. Parte 1 - Accesso ad Azure DevOps

Apri il browser e accedi al portale Azure DevOps.

Usa l'account indicato dal docente o quello disponibile per il laboratorio.

Dopo l'accesso verifica di essere nella pagina principale di Azure DevOps.

Devi ottenere una situazione di questo tipo:

```text
https://dev.azure.com/NOME_ORGANIZZAZIONE
```

Se arrivi già dentro una organizzazione esistente, non crearne un'altra senza indicazione del docente.

---

# 5. Parte 2 - Creazione o verifica dell'organizzazione

## 5.1 Caso A - Non hai ancora una organizzazione

Crea una nuova organizzazione Azure DevOps.

Valori consigliati:

| Campo | Valore suggerito |
|---|---|
| Organization name | `academy-observability-nomecognome` |
| Region | Europa, se selezionabile |
| Account | quello indicato dal docente |

Dopo la creazione, annota la URL.

Esempio:

```text
https://dev.azure.com/academy-observability-mariorossi
```

## 5.2 Caso B - Hai già una organizzazione

Aprila e verifica di poter accedere almeno a:

- Organization settings;
- elenco progetti;
- creazione nuovo progetto oppure progetto assegnato dal docente.

Se non hai permessi sufficienti, segnalo subito al docente.

---

# 6. Parte 3 - Creazione del progetto

Dalla home dell'organizzazione crea un nuovo progetto.

Valori consigliati:

| Campo | Valore |
|---|---|
| Project name | `Observability-DevOps` |
| Visibility | `Private` |
| Version control | `Git` |
| Work item process | `Basic` |

Anche se useremo GitHub come repository principale, il progetto Azure DevOps può restare configurato con version control Git.

Il progetto ci serve soprattutto per:

- pipeline;
- impostazioni;
- service connection;
- eventuali controlli futuri.

---

# 7. Parte 4 - Verifica delle sezioni principali

Apri il progetto appena creato.

Verifica di poter entrare in queste sezioni.

## 7.1 Overview

Serve a verificare che il progetto sia stato creato correttamente.

Annota:

```text
Nome organizzazione:
Nome progetto:
URL progetto:
```

## 7.2 Pipelines

Apri la sezione:

```text
Pipelines
```

Per ora non creare una pipeline se il docente non lo richiede.

Devi solo verificare che la sezione sia accessibile.

## 7.3 Project settings

Apri:

```text
Project settings
```

Questa sezione sarà importante nelle UD successive.

## 7.4 Service connections

Dentro Project settings cerca:

```text
Service connections
```

Per ora devi solo localizzare il punto in cui saranno create le connessioni.

Nelle prossime UD useremo service connection per:

- collegare GitHub;
- collegare Azure Resource Manager;
- consentire alle pipeline di operare sulle risorse Azure.

---

# 8. Parte 5 - Verifica account e permessi

Compila questa tabella nel tuo file di evidenza.

| Controllo | Esito |
|---|---|
| Accedo ad Azure DevOps | sì/no |
| Vedo la mia organizzazione | sì/no |
| Vedo il progetto `Observability-DevOps` | sì/no |
| Posso aprire Pipelines | sì/no |
| Posso aprire Project settings | sì/no |
| Vedo Service connections | sì/no |
| So quale account sto usando | sì/no |

Se una risposta è `no`, indica il problema.

---

# 9. Parte 6 - Collegamento logico con GitHub

In questa UD non colleghiamo ancora un repository operativo alla pipeline.

Però devi verificare di avere accesso a GitHub e sapere quale account userai.

Annota:

```text
Account GitHub usato nel corso:
Organizzazione o repository GitHub usato nel corso:
Metodo di accesso GitHub:
```

Questa informazione sarà utile quando creeremo pipeline partendo da repository GitHub.

---

# 10. Parte 7 - Collegamento logico con Azure

In UD05 hai già lavorato con risorse Azure o con risorse predisposte dal docente.

In questa UD devi solo annotare quali risorse potranno essere coinvolte più avanti.

Compila se conosci i valori.

```text
Subscription Azure:
Resource Group principale:
Regione prevalente:
Log Analytics Workspace usato nel percorso:
Eventuale ACR già esistente:
```

Se un valore non è ancora disponibile, scrivi:

```text
Da definire nelle UD successive
```

Non inventare nomi.

---

# 11. File di evidenza richiesto

Crea il file:

```bash
mkdir -p docs
code docs/evidence_ud11_setup_azure_devops.md
```

Se non usi VS Code, crea comunque un file Markdown equivalente.

Inserisci questa struttura:

```md
# Evidence UD11 - Setup Azure DevOps

## 1. Dati generali
- Nome organizzazione Azure DevOps:
- URL organizzazione:
- Nome progetto:
- URL progetto:

## 2. Account usati
- Account Azure DevOps:
- Account GitHub:
- Account Azure / subscription, se nota:

## 3. Verifiche portale Azure DevOps
| Controllo | Esito | Note |
|---|---|---|
| Accesso organizzazione |  |  |
| Accesso progetto |  |  |
| Accesso Pipelines |  |  |
| Accesso Project settings |  |  |
| Visualizzazione Service connections |  |  |

## 4. Collegamento con UD successive
Spiego con parole mie perché questa UD prepara le pipeline delle UD successive.

## 5. Dubbi o problemi
Indico eventuali problemi incontrati.
```

---

# 12. Cosa devi saper spiegare al docente

Al termine del laboratorio devi saper dire:

```text
Ho creato o verificato una organizzazione Azure DevOps.
Ho creato o verificato il progetto Observability-DevOps.
So dove si trovano Pipelines e Project settings.
So che le service connection serviranno alle pipeline per collegarsi a GitHub e Azure.
In questa UD non abbiamo fatto deploy: abbiamo preparato il contenitore operativo per il ciclo DevOps delle UD successive.
```

---

# 13. Troubleshooting minimo

## 13.1 Non riesco ad accedere ad Azure DevOps

Possibili cause:

- account errato;
- sessione browser con utente sbagliato;
- conflitto tra account personale e account aziendale;
- accesso non autorizzato.

Prova prima da finestra anonima o da browser pulito.

## 13.2 Non vedo il progetto

Possibili cause:

- sei nell'organizzazione sbagliata;
- il progetto non è stato creato;
- non hai permessi sul progetto;
- stai usando un account diverso.

## 13.3 Non vedo Project settings

Possibile causa:

- permessi insufficienti.

In questo caso segnalo al docente, perché nelle UD successive Project settings sarà necessario.

## 13.4 Non vedo Service connections

Possibili cause:

- permessi insufficienti;
- progetto non corretto;
- interfaccia Azure DevOps aperta in sezione sbagliata.

---

# 14. Conclusione

Questo laboratorio non produce ancora un deploy.

Produce però una base fondamentale:

```text
Azure DevOps è pronto.
Il progetto è pronto.
Sappiamo dove saranno create le pipeline.
Sappiamo dove saranno create le service connection.
Sappiamo come questo si collegherà a GitHub e Azure.
```

Da questo punto in poi potremo iniziare a trasformare il lavoro manuale già visto su Azure in un ciclo DevOps automatizzato.
