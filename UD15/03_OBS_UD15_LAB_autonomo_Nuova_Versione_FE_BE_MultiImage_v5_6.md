# UD15 - Laboratorio autonomo
## Nuova versione FE/BE e immagini multi-image

## Scenario

Devi rilasciare una nuova versione didattica del sistema FE/BE, senza fare deploy cloud.

L'obiettivo è dimostrare che sai modificare il codice, ricostruire le immagini, rilanciare la pipeline e verificare i nuovi tag in ACR.

## Attività

1. Modifica `APP_VERSION` di frontend e backend da `1.0.0` a `1.1.0-ud15` usando variabili d'ambiente nel test locale oppure modificando i Dockerfile.
2. Ricostruisci localmente entrambe le immagini:

```bash
docker build -t backend:ud15-1.1 ./backend
docker build -t frontend:ud15-1.1 ./frontend
```

3. Avvia backend e frontend in rete Docker.
4. Verifica:

```bash
curl http://127.0.0.1:8001/version
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/demo
```

5. Esegui commit e push.
6. Rilancia la pipeline UD15.
7. Verifica in ACR che `backend` e `frontend` abbiano un nuovo tag.
8. Documenta le evidenze.

## Evidenze minime

Nel file `docs/evidence_ud15_autonomo.md` inserisci:

- comando di build locale delle due immagini;
- output di `/version` per backend e frontend;
- output di `/demo`;
- identificativo del run pipeline;
- tag ACR di backend e frontend;
- breve spiegazione della differenza tra immagine frontend e immagine backend.

## Criterio di successo

Il laboratorio è completato quando puoi mostrare:

```text
stesso Build ID pipeline
-> tag backend in ACR
-> tag frontend in ACR
```
