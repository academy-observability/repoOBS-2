# UD16 - Raccordo finale
## Dal multi-image al deploy cloud FE/BE

## 1. Cosa abbiamo completato

Con UD16 abbiamo trasformato le immagini prodotte in UD15 in servizi cloud eseguibili.

```text
UD15:
frontend code -> frontend image -> ACR
backend code  -> backend image  -> ACR

UD16:
ACR/frontend:<tag> -> Frontend Container App
ACR/backend:<tag>  -> Backend Container App
```

## 2. Cosa cambia rispetto a UD13/UD14

| UD | Target | Tipo applicazione |
|---|---|---|
| UD13 | ACI | app singola |
| UD14 | ACI | app singola con pipeline multistage |
| UD16 | ACA | sistema FE/BE |

UD16 introduce un runtime più adatto a servizi applicativi composti da più container.

## 3. Cosa prepara UD17

Ora che frontend e backend sono in cloud, possiamo osservare:

- richieste HTTP;
- dipendenze frontend -> backend;
- errori applicativi;
- log runtime;
- tempi di risposta;
- revisioni e cambiamenti.

Questo prepara UD17:

```text
Observability cloud post-deploy con Azure Monitor, Application Insights, Log Analytics e KQL.
```

## 4. Concetto da ricordare

> Il deploy non è concluso quando Azure crea la risorsa. Il deploy è concluso quando il servizio risponde, le dipendenze funzionano e abbiamo evidenze consultabili.
