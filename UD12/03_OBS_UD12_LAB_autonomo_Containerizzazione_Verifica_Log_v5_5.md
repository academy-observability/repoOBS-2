# UD12 - Laboratorio autonomo
## Containerizzazione, porta alternativa, verifica HTTP e log

---

# 1. Scenario

Hai già costruito e avviato una applicazione containerizzata nel laboratorio guidato.

Ora devi dimostrare di saper ripetere il flusso con maggiore autonomia, usando:

- una nuova immagine;
- un nuovo nome container;
- una porta esterna diversa;
- test HTTP;
- lettura e commento dei log.

---

# 2. Obiettivo operativo

Alla fine del laboratorio autonomo devi avere:

- immagine `obsapp-ud12:autonomo`;
- container `obsapp-ud12-autonomo`;
- mapping porta `8001:8000`;
- endpoint verificati da `http://127.0.0.1:8001`;
- log letti con `docker logs`;
- evidenze documentate.

---

# 3. Preparazione

Vai nella cartella della UD12:

```bash
cd ~/corso_obs/work/UD12
```

Verifica i file:

```bash
find . -maxdepth 2 -type f | sort
```

Devono essere presenti almeno:

```text
./Dockerfile
./requirements.txt
./src/app.py
```

---

# 4. Build nuova immagine

Costruisci una nuova immagine:

```bash
docker build -t obsapp-ud12:autonomo .
```

Verifica:

```bash
docker images | grep obsapp-ud12
```

---

# 5. Avvio container su porta alternativa

Rimuovi eventuali container precedenti con lo stesso nome:

```bash
docker rm -f obsapp-ud12-autonomo 2>/dev/null || true
```

Avvia:

```bash
docker run -d --name obsapp-ud12-autonomo -p 8001:8000 obsapp-ud12:autonomo
```

Verifica:

```bash
docker ps
```

Nota importante:

```text
La porta esterna è 8001.
La porta interna del container è 8000.
Quindi i test dal PC devono usare http://127.0.0.1:8001
```

---

# 6. Test endpoint

Esegui:

```bash
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8001/time
curl -X POST http://127.0.0.1:8001/echo \
  -H 'Content-Type: application/json' \
  -d '{"lab":"UD12","activity":"autonomo"}'
curl http://127.0.0.1:8001/error
curl http://127.0.0.1:8001/non-esiste
```

Risultati attesi:

| Endpoint | Esito atteso |
|---|---|
| `/` | `200` |
| `/health` | `200` |
| `/time` | `200` |
| `/echo` | `200` |
| `/error` | `500` simulato |
| `/non-esiste` | `404` |

---

# 7. Lettura log

Leggi i log:

```bash
docker logs obsapp-ud12-autonomo
```

Individua almeno tre righe rilevanti:

- una richiesta corretta;
- una richiesta con errore simulato `500`;
- una richiesta a rotta inesistente `404`.

---

# 8. Evidenza richiesta

Crea:

```bash
code docs/evidence_ud12_autonomo.md
```

Compila:

```md
# Evidence UD12 - Laboratorio autonomo

## 1. Immagine costruita
Comando usato e output essenziale di docker images.

## 2. Container avviato
Comando usato e output di docker ps.

## 3. Mapping porta
Spiego perché uso http://127.0.0.1:8001.

## 4. Test HTTP
Incollo output di:
- /
- /health
- /time
- /echo
- /error
- /non-esiste

## 5. Log
Incollo alcune righe di docker logs.

## 6. Commento tecnico
Spiego cosa dimostrano i log e quale differenza c'è tra status 200, 404 e 500.

## 7. Cleanup
Indico se ho rimosso il container oppure se l'ho lasciato attivo per verifica docente.
```

---

# 9. Cleanup

A fine prova, se richiesto dal docente:

```bash
docker rm -f obsapp-ud12-autonomo
```

Non rimuovere l'immagine se il docente vuole controllarla successivamente.

---

# 10. Criteri di riuscita

Il laboratorio autonomo è riuscito se puoi dimostrare:

- container attivo;
- endpoint raggiungibili sulla porta corretta;
- log coerenti con le richieste eseguite;
- differenza tra porta esterna e porta interna;
- differenza tra immagine e container.
