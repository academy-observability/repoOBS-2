# UD12 - Concetti
## Docker locale: singola applicazione containerizzata e osservabile

---

# 1. Scopo della UD

Nella UD precedente abbiamo introdotto il ciclo DevOps e il ruolo di repository, pipeline, artifact, registry, deploy e verifica.

In questa UD ci concentriamo su un elemento preciso di quel ciclo: **l'immagine container**.

L'obiettivo non è ancora distribuire un'applicazione in cloud. L'obiettivo è capire bene cosa accade quando trasformiamo una piccola applicazione locale in un'immagine Docker e poi la eseguiamo come container.

La sequenza tecnica della UD è questa:

```text
codice sorgente
   -> Dockerfile
   -> docker build
   -> immagine
   -> docker run
   -> container
   -> test HTTP
   -> log
```

---

# 2. Perché Docker entra nel percorso Observability

Docker non è uno strumento di observability. È uno strumento di packaging ed esecuzione.

Però è importante per l'observability perché rende più ripetibile il modo in cui una applicazione viene eseguita.

Quando un'applicazione gira dentro un container, possiamo ragionare in modo più ordinato su:

- quale codice è stato impacchettato;
- quale runtime viene usato;
- quale porta espone il servizio;
- quali log vengono prodotti;
- quale versione dell'immagine è in esecuzione;
- come verificare se il servizio risponde.

Quindi Docker non sostituisce log, metriche e trace. Docker rende più disciplinato il modo in cui portiamo un'applicazione in esecuzione.

---

# 3. Applicazione, immagine e container

Uno degli errori più comuni è confondere questi tre livelli.

| Oggetto | Significato |
|---|---|
| Codice sorgente | File dell'applicazione, ad esempio `app.py` |
| Immagine Docker | Pacchetto eseguibile costruito a partire dal codice e dal Dockerfile |
| Container | Istanza in esecuzione di una immagine |

Una immagine può essere usata per creare più container.

Un container può essere fermato o eliminato senza eliminare necessariamente l'immagine.

---

# 4. Che cos'è un Dockerfile

Il `Dockerfile` è il file che descrive come costruire l'immagine.

Nel nostro laboratorio conterrà istruzioni come:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/app.py /app/app.py
EXPOSE 8000
ENV PORT=8000
CMD ["python", "app.py"]
```

## 4.1 Lettura riga per riga

| Istruzione | Significato |
|---|---|
| `FROM` | indica l'immagine base da cui partire |
| `WORKDIR` | imposta la directory di lavoro interna |
| `COPY` | copia file dal progetto locale nell'immagine |
| `RUN` | esegue comandi durante la build |
| `EXPOSE` | documenta la porta usata dall'applicazione |
| `ENV` | definisce una variabile d'ambiente |
| `CMD` | indica il comando eseguito all'avvio del container |

Il Dockerfile non avvia il container. Serve a costruire l'immagine.

---

# 5. Che cos'è una immagine Docker

Una immagine Docker è un pacchetto eseguibile che contiene tutto ciò che serve per avviare l'applicazione:

- base operating system minimale;
- runtime Python;
- librerie;
- codice applicativo;
- comando di avvio.

L'immagine viene costruita con:

```bash
docker build -t obsapp-ud12:1.0 .
```

Il tag `obsapp-ud12:1.0` serve a dare un nome e una versione locale all'immagine.

---

# 6. Che cos'è un container

Un container è una istanza in esecuzione di una immagine.

Esempio:

```bash
docker run --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
```

Qui stiamo dicendo:

- crea un container chiamato `obsapp-ud12`;
- collega la porta `8000` del computer alla porta `8000` interna del container;
- usa l'immagine `obsapp-ud12:1.0`.

---

# 7. Mapping delle porte

Il parametro:

```bash
-p 8000:8000
```

va letto così:

```text
porta_del_PC:porta_del_container
```

Quindi:

```text
8000 esterna -> 8000 interna
```

Se invece uso:

```bash
-p 8001:8000
```

allora devo chiamare l'app dal PC su:

```text
http://127.0.0.1:8001
```

ma dentro il container l'app continua ad ascoltare sulla porta `8000`.

---

# 8. Foreground e detached mode

Un container può essere avviato in foreground:

```bash
docker run --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
```

In questo caso il terminale resta occupato e mostra direttamente l'output del processo.

Oppure può essere avviato in background, cioè in modalità detached:

```bash
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
```

In questo caso il terminale torna disponibile e possiamo leggere i log con:

```bash
docker logs obsapp-ud12
```

---

# 9. Log del container

Nel nostro laboratorio l'applicazione scrive log JSON su stdout.

Docker raccoglie questi log e li rende visibili con:

```bash
docker logs obsapp-ud12
```

Campi utili:

| Campo | Significato |
|---|---|
| `timestamp` | momento della richiesta |
| `level` | livello logico del log |
| `request_id` | identificativo della richiesta |
| `method` | metodo HTTP |
| `path` | endpoint chiamato |
| `status` | codice HTTP restituito |
| `latency_ms` | tempo di risposta |

Questo collega Docker al tema Observability: anche dentro un container l'applicazione deve continuare a produrre segnali leggibili.

---

# 10. Modifica del codice e rebuild

Se cambio il codice sorgente, il container già avviato non si aggiorna da solo.

La sequenza corretta è:

```text
modifico il codice
   -> ricostruisco l'immagine
   -> elimino o fermo il vecchio container
   -> avvio un nuovo container dalla nuova immagine
   -> verifico il comportamento
```

Esempio:

```bash
docker build -t obsapp-ud12:1.1 .
docker rm -f obsapp-ud12
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.1
```

---

# 11. Che cosa non facciamo in questa UD

Per mantenere chiaro il focus, in questa UD non introduciamo ancora:

- pipeline operative;
- registry remoto;
- deploy su Azure;
- più container collegati tra loro;
- Docker Compose;
- Prometheus;
- Grafana;
- Application Insights.

Questa UD serve a rendere solida la base locale.

---

# 12. Mappa mentale finale

```text
Codice sorgente
   -> Dockerfile
   -> Immagine Docker
   -> Container
   -> Porta esposta
   -> Endpoint HTTP
   -> Log
   -> Evidenza tecnica
```

Se questa mappa è chiara, il partecipante è pronto a capire perché una pipeline può costruire automaticamente una immagine e usarla come unità di rilascio.
