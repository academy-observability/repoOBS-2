# UD15 - Concetti
## FE/BE, monorepo, due immagini Docker e pubblicazione su ACR

## 1. Scopo della UD15

Nelle UD precedenti abbiamo lavorato su una singola applicazione containerizzata:

```text
UD12  -> Docker locale su app singola
UD13  -> primo deploy automatico app singola su ACR/ACI
UD14  -> pipeline multistage app singola con smoke test
```

In UD15 facciamo un salto architetturale: non lavoriamo più su una sola applicazione, ma su due componenti distinti:

```text
Client -> Frontend -> Backend
```

L'obiettivo non è ancora il deploy finale del sistema FE/BE nel cloud. L'obiettivo è preparare correttamente il progetto:

- un repository unico, cioè un monorepo;
- due cartelle applicative distinte;
- due Dockerfile;
- due immagini Docker;
- una pipeline Azure DevOps capace di costruire e pubblicare entrambe le immagini in Azure Container Registry.

## 2. Monorepo non significa monolite

Un errore frequente è confondere monorepo e monolite.

| Termine | Significato nel corso |
|---|---|
| Monorepo | Un solo repository GitHub contiene più componenti dello stesso sistema. |
| Monolite | Una sola applicazione contiene tutte le responsabilità. |
| FE/BE | Due servizi distinti, anche se conservati nello stesso repository. |

Nel nostro caso avremo un solo repository, ma due servizi:

```text
work/UD15/
├── frontend/
└── backend/
```

## 3. Perché servono due immagini

Frontend e backend hanno ruoli diversi e devono essere gestiti come unità distribuibili distinte.

Il backend espone endpoint di servizio, ad esempio:

- `/health`;
- `/version`;
- `/work`;
- `/work-error`.

Il frontend espone endpoint per il client e chiama il backend, ad esempio:

- `/health`;
- `/ready`;
- `/version`;
- `/demo`;
- `/demo-error`.

Per questo motivo avremo due immagini:

```text
NOME_ACR.azurecr.io/backend:<tag>
NOME_ACR.azurecr.io/frontend:<tag>
```

## 4. Ruolo di Azure Container Registry

ACR non contiene codice sorgente. Contiene immagini container.

Nel nostro percorso:

```text
GitHub = codice
Azure DevOps = pipeline
ACR = immagini container
```

In UD15 la pipeline costruisce due immagini e le pubblica in ACR. Il deploy su una piattaforma runtime arriverà in un passaggio successivo del percorso.

## 5. Ruolo di Azure DevOps

In UD15 Azure DevOps non deploya ancora frontend e backend. Esegue invece una pipeline multi-image:

```text
ValidateRepository
-> PublishImages
   -> BuildBackend
   -> BuildFrontend
```

Questo è importante perché separa due responsabilità:

- preparare immagini corrette e tracciabili;
- distribuire tali immagini in un ambiente runtime.

UD15 si concentra sulla prima responsabilità.

## 6. Perché facciamo anche test locale

Prima di affidare tutto alla pipeline, verifichiamo localmente che frontend e backend funzionino.

La verifica locale serve a distinguere:

| Problema | Dove si intercetta meglio |
|---|---|
| errore nel codice Python | test locale / ValidateRepository |
| Dockerfile errato | build locale o build pipeline |
| collegamento FE -> BE errato | test locale con rete Docker |
| push ACR errato | stage pipeline PublishImages |

## 7. Concetto chiave della UD15

La frase da ricordare è:

```text
In UD15 non stiamo ancora distribuendo il sistema FE/BE nel cloud.
Stiamo preparando due immagini affidabili e tracciabili che potranno essere usate da un deploy successivo.
```

## 8. Semplificazioni didattiche

In questa UD:

- usiamo due servizi Python semplici;
- usiamo due Dockerfile separati;
- usiamo un ACR già creato o verificato;
- non introduciamo ancora Azure Container Apps;
- non introduciamo ancora Application Insights;
- non usiamo GitHub Actions;
- non usiamo App Service for Containers.

Questa scelta evita di moltiplicare strumenti e target prima che il modello FE/BE sia chiaro.
