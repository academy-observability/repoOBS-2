# OBS UD12 - Approfondimento
## Differenza tra l'app osservabile UD04 e l'app Flask usata in UD12

Versione: v5.5 REV  
Destinatari: partecipanti  
Tipo documento: approfondimento concettuale  

---

# 1. Perché questo approfondimento

In UD04 abbiamo già lavorato con un piccolo servizio HTTP osservabile, contenuto nel file:

```text
observable_service.py
```

In UD12 usiamo invece una piccola applicazione Python basata su Flask.

A prima vista le due applicazioni sembrano simili, perché entrambe:

- espongono endpoint HTTP;
- rispondono in JSON;
- hanno un endpoint di health check;
- generano errori controllati;
- producono log utili per l'osservabilità;
- possono essere avviate da terminale.

La domanda corretta è quindi:

```text
Perché in UD12 usiamo una app diversa da quella vista in UD04?
```

La risposta breve è questa:

```text
In UD04 l'obiettivo era costruire un primo servizio osservabile usando solo Python standard.
In UD12 l'obiettivo è containerizzare una piccola API più vicina a uno scenario applicativo moderno.
```

La differenza non è quindi solo nel codice, ma nello scopo didattico.

---

# 2. Scopo dell'app UD04

L'app di UD04 è stata pensata come primo servizio osservabile locale.

Il suo obiettivo principale era mostrare che un servizio può produrre segnali utili anche senza strumenti complessi.

In UD04 i partecipanti dovevano concentrarsi su concetti come:

- servizio HTTP locale;
- endpoint `/health`;
- endpoint `/ready`;
- endpoint `/metrics`;
- generazione di log JSON;
- simulazione di lavoro con `/work`;
- simulazione di errore con `/fail`;
- lettura del file di log;
- prime metriche applicative minime.

Il punto importante era:

```text
un'applicazione osservabile produce segnali tecnici leggibili.
```

Per questo motivo l'app UD04 usa solo la libreria standard Python.

Non richiede framework esterni e non richiede un file `requirements.txt`.

---

# 3. Scopo dell'app UD12

L'app UD12 è stata pensata per un obiettivo diverso: lavorare con Docker.

In UD12 non vogliamo insegnare di nuovo che cos'è un servizio osservabile. Questo concetto è già stato introdotto.

Vogliamo invece far vedere come una piccola applicazione possa essere trasformata in una immagine Docker e poi avviata come container.

La sequenza didattica è:

```text
codice sorgente
   -> dipendenze
   -> Dockerfile
   -> docker build
   -> immagine Docker
   -> docker run
   -> container
   -> test HTTP
   -> docker logs
```

Per questo motivo l'app UD12 usa Flask.

Flask permette di scrivere una piccola API HTTP in modo molto leggibile, con endpoint chiari e facilmente testabili tramite `curl`.

Il punto importante della UD12 è:

```text
la stessa applicazione può essere eseguita localmente oppure dentro un container.
```

---

# 4. Differenza tecnica principale

La differenza tecnica principale è questa:

| Aspetto | App UD04 | App UD12 |
|---|---|---|
| Tipo di applicazione | Servizio HTTP scritto con libreria standard Python | API HTTP scritta con Flask |
| Dipendenze esterne | Nessuna | Flask |
| File `requirements.txt` | Non necessario | Necessario |
| Server HTTP | `HTTPServer` / `BaseHTTPRequestHandler` | Flask / Werkzeug |
| Focus principale | Observability locale | Containerizzazione Docker |
| Log | File locale | stdout, leggibile con `docker logs` |
| Metriche | Endpoint `/metrics` | Non centrale in questa UD |
| Readiness | Endpoint `/ready` | Non centrale in questa UD |

Quindi le due app non sono in contraddizione.

Servono a due momenti diversi del percorso.

---

# 5. Perché in UD12 importiamo Flask

Nell'app UD12 troviamo:

```python
from flask import Flask, g, jsonify, request
```

Questo import serve perché Flask fornisce le funzionalità di base per costruire una piccola API HTTP.

In particolare:

| Oggetto Flask | A cosa serve |
|---|---|
| `Flask` | crea l'applicazione web |
| `jsonify` | restituisce risposte JSON corrette |
| `request` | permette di leggere metodo, path, header e body della richiesta |
| `g` | conserva dati validi solo per la richiesta corrente |

Esempio:

```python
@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200
```

Questa sintassi permette di dire in modo leggibile:

```text
quando arriva una richiesta GET su /health, esegui questa funzione.
```

Senza Flask dovremmo gestire manualmente path, metodi HTTP, header e body, come avviene nell'app UD04.

---

# 6. Differenza sugli endpoint

## 6.1 Endpoint principali dell'app UD04

L'app UD04 espone endpoint come:

```text
/health
/ready
/time
/work?ms=...
/fail
/metrics
/echo
```

Questi endpoint sono molto utili per introdurre il concetto di servizio osservabile.

In particolare:

- `/ready` introduce la readiness;
- `/metrics` introduce metriche applicative minime;
- `/work?ms=...` simula latenza controllata;
- `/fail` genera un errore controllato;
- `/echo` permette di provare una richiesta POST.

## 6.2 Endpoint principali dell'app UD12

L'app UD12 espone endpoint più semplici:

```text
/
/health
/time
/echo
/error
```

Questi endpoint sono sufficienti per il lavoro della UD12, perché permettono di verificare:

- risposta corretta `200`;
- richiesta POST;
- errore simulato `500`;
- rotta inesistente `404`;
- produzione di log leggibili dal container.

Il focus non è aumentare il numero di endpoint.

Il focus è capire che l'applicazione, una volta containerizzata, continua a rispondere e a produrre log.

---

# 7. Differenza sui log

La differenza sui log è molto importante.

## 7.1 Log nell'app UD04

L'app UD04 scrive i log in un file locale, per esempio:

```text
logs/app.log
```

Questo era coerente con UD04, perché lì l'obiettivo era lavorare con log locali e comandi come:

```bash
cat logs/app.log
tail -f logs/app.log
grep ERROR logs/app.log
```

In quel momento il partecipante doveva capire che un servizio può produrre file di log analizzabili.

## 7.2 Log nell'app UD12

L'app UD12 scrive invece i log su stdout tramite:

```python
print(json.dumps(record), flush=True)
```

Questa scelta è coerente con Docker.

Quando un'app dentro un container scrive su stdout o stderr, Docker rende quei log disponibili con:

```bash
docker logs nome-container
```

Quindi in UD12 il partecipante deve capire questa catena:

```text
richiesta HTTP
   -> app dentro container
   -> log scritto su stdout
   -> docker logs
   -> evidenza tecnica
```

La scelta non significa che il log su file sia sbagliato.

Significa che, in un laboratorio Docker, è più diretto usare stdout/stderr per leggere i log del container.

---

# Conclusione operativa

L'app UD04 e l'app UD12 sono entrambe corrette, ma servono a scopi diversi.

```text
UD04 = capire che cos'è un servizio osservabile locale.
UD12 = capire come una piccola API viene containerizzata ed eseguita con Docker.
```

Per la UD12 manteniamo quindi l'app Flask prevista nei materiali.

Non stiamo sostituendo l'app UD04 perché fosse sbagliata. Stiamo usando una app più adatta a mostrare:

- dipendenze applicative;
- file `requirements.txt`;
- `Dockerfile`;
- build dell'immagine;
- run del container;
- mapping porte;
- log tramite `docker logs`.

La continuità concettuale resta questa:

```text
UD04: un servizio produce segnali osservabili.
UD12: un servizio containerizzato continua a produrre segnali osservabili.
```
