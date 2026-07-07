# UD12 - Mini-attività
## Immagine, container, porta e log

---

# 1. Obiettivo

Questa mini-attività serve a verificare che il partecipante non abbia solo eseguito comandi Docker, ma abbia capito il flusso tecnico.

Il punto da ricostruire è:

```text
codice sorgente
   -> Dockerfile
   -> docker build
   -> immagine
   -> docker run
   -> container
   -> porta esposta
   -> endpoint HTTP
   -> log
```

---

# 2. Attività richiesta

Completa le risposte in modo sintetico ma preciso.

## 2.1 Codice sorgente

Dove si trova il codice dell'applicazione?

Risposta:

```text
...
```

## 2.2 Dockerfile

Quale file descrive come costruire l'immagine?

Risposta:

```text
...
```

## 2.3 Build

Che cosa produce il comando seguente?

```bash
docker build -t obsapp-ud12:1.0 .
```

Risposta:

```text
...
```

## 2.4 Immagine

Come verifichi che l'immagine esista localmente?

Risposta:

```text
...
```

## 2.5 Container

Che cosa produce il comando seguente?

```bash
docker run -d --name obsapp-ud12 -p 8000:8000 obsapp-ud12:1.0
```

Risposta:

```text
...
```

## 2.6 Porta

Nel mapping `-p 8001:8000`, quale porta devi usare dal browser o da `curl` sul tuo PC?

Risposta:

```text
...
```

## 2.7 Log

Con quale comando leggi i log del container?

Risposta:

```text
...
```

## 2.8 Differenza immagine/container

Spiega in massimo cinque righe la differenza tra immagine Docker e container.

Risposta:

```text
...
```

## 2.9 Collegamento con DevOps

Perché una immagine Docker è utile in un flusso DevOps automatizzato?

Risposta:

```text
...
```

---

# 3. Consegna

Salva le risposte in:

```text
docs/mini_attivita_ud12.md
```

Poi esegui:

```bash
git add docs/mini_attivita_ud12.md
git commit -m "UD12 - Mini attività immagine container log"
```

Se il docente chiede la consegna su repository remoto, esegui anche:

```bash
git push
```
