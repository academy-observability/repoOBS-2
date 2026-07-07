# UD12 - Guida operativa
## Comandi Docker base e troubleshooting

---

# 1. Verifica Docker

```bash
docker --version
docker version
docker info
```

Test rapido:

```bash
docker run hello-world
```

---

# 2. Immagini

Elenco immagini:

```bash
docker images
```

Build immagine:

```bash
docker build -t nome-immagine:tag .
```

Esempio:

```bash
docker build -t obsapp-ud12:1.0 .
```

Rimozione immagine:

```bash
docker rmi nome-immagine:tag
```

---

# 3. Container

Avvio in foreground:

```bash
docker run --name nome-container -p 8000:8000 nome-immagine:tag
```

Avvio in background:

```bash
docker run -d --name nome-container -p 8000:8000 nome-immagine:tag
```

Elenco container attivi:

```bash
docker ps
```

Elenco tutti i container:

```bash
docker ps -a
```

Stop:

```bash
docker stop nome-container
```

Start:

```bash
docker start nome-container
```

Restart:

```bash
docker restart nome-container
```

Rimozione forzata:

```bash
docker rm -f nome-container
```

---

# 4. Porte

Forma generale:

```bash
-p porta_pc:porta_container
```

Esempi:

```bash
-p 8000:8000
```

Il PC chiama:

```text
http://127.0.0.1:8000
```

```bash
-p 8001:8000
```

Il PC chiama:

```text
http://127.0.0.1:8001
```

Dentro il container l'app continua ad ascoltare sulla porta `8000`.

---

# 5. Log

Lettura log:

```bash
docker logs nome-container
```

Ultime righe:

```bash
docker logs --tail 20 nome-container
```

Log in follow:

```bash
docker logs -f nome-container
```

---

# 6. Ispezione container

Dettagli container:

```bash
docker inspect nome-container
```

Processi nel container:

```bash
docker top nome-container
```

Uso risorse:

```bash
docker stats nome-container
```

---

# 7. Troubleshooting rapido

## 7.1 Docker non risponde

Sintomo:

```text
Cannot connect to the Docker daemon
```

Verifiche:

```bash
docker info
```

Possibili cause:

- Docker Desktop non avviato;
- servizio Docker non attivo;
- terminale WSL non integrato con Docker Desktop.

---

## 7.2 Porta già occupata

Sintomo:

```text
Bind for 0.0.0.0:8000 failed: port is already allocated
```

Verifiche:

```bash
docker ps
```

Soluzioni:

```bash
docker rm -f obsapp-ud12
```

oppure usare una porta diversa:

```bash
docker run -d --name obsapp-ud12-alt -p 8001:8000 obsapp-ud12:1.0
```

---

## 7.3 Container si chiude subito

Verifica:

```bash
docker ps -a
docker logs nome-container
```

Possibili cause:

- errore Python;
- file mancante;
- dipendenza non installata;
- comando `CMD` errato.

---

## 7.4 Curl non risponde

Verifiche:

```bash
docker ps
docker logs nome-container
```

Controllare soprattutto:

- nome container;
- porta esterna;
- porta interna;
- app effettivamente avviata.

---

## 7.5 Vedo ancora la vecchia versione

Possibili cause:

- immagine non ricostruita;
- container avviato da vecchio tag;
- container precedente non rimosso.

Sequenza consigliata:

```bash
docker build -t obsapp-ud12:1.1 .
docker rm -f obsapp-ud12
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.1
```

---

# 8. Comandi utili di pulizia

Rimuovere container fermati:

```bash
docker container prune
```

Rimuovere immagini non usate:

```bash
docker image prune
```

Attenzione: usare i comandi `prune` solo se il docente li autorizza.
