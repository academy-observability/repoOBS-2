# UD30 — Dal Machine Learning agli LLM

## Perché questa unità arriva dopo UD29

Nella UD29 il Decision Tree riceveva feature e produceva una classe:

```text
status_code = 500
duration_ms = 1800
error_count = 7
        ↓
Decision Tree
        ↓
anomalia = sì
```

Nella UD30 un LLM riceve testo e istruzioni:

```text
evidence packet + prompt
        ↓
LLM
        ↓
sintesi, spiegazioni, ipotesi e verifiche proposte
```

Il testo può apparire convincente senza essere dimostrato. Per questo la nuova competenza non è soltanto “usare una chat”, ma **vincolare e verificare l'output**.

## 1. Classe strutturata e risposta generativa

Un Decision Tree sceglie una classe appartenente a un insieme già definito:

```text
normal | anomaly
```

La previsione può essere confrontata con una reference label e valutata con precision, recall e altre metriche.

Un LLM genera invece una sequenza di token. L'output può contenere:

- fatti ripresi dal prompt;
- sintesi corrette;
- inferenze plausibili;
- dettagli non forniti;
- conclusioni espresse con eccessiva sicurezza.

**La forma linguistica non certifica il contenuto.**

## 2. Che cos'è un LLM

Un Large Language Model è un modello addestrato su grandi quantità di testo per elaborare sequenze linguistiche e generare continuazioni coerenti con il contesto ricevuto.

Non è:

- un database di risposte già scritte;
- un motore che vede automaticamente il sistema osservato;
- una fonte sempre corretta;
- una prova tecnica.

## 3. Token

Il modello non elabora direttamente “parole” nel senso comune. Elabora token, che possono corrispondere a:

- una parola;
- una parte di parola;
- punteggiatura;
- numeri o simboli;
- sequenze frequenti.

```text
prompt → token di input → modello → token di output → risposta
```

Il numero di token è rilevante perché influenza:

- quantità di testo elaborata;
- memoria usata per il contesto;
- tempo di generazione;
- consumo di CPU/GPU;
- costo nei servizi che tariffano l'uso;
- quantità di telemetria da osservare.

## 4. Addestramento e inferenza

### Addestramento

Durante l'addestramento il modello modifica i propri parametri usando esempi e un processo di ottimizzazione.

### Inferenza

Durante l'inferenza il modello già addestrato riceve un input e produce un output.

```text
addestramento → costruisce/modifica il modello
inferenza     → usa il modello
```

In questa UD non addestriamo un LLM. Eseguiamo inferenze con modelli già disponibili.

## 5. Perché una risposta convincente non è una prova

Esempio di risposta:

> Il database è saturo e causa la latenza del Catalogo.

Questa frase non è una prova se l'evidence packet non contiene:

- metriche del database;
- trace verso il database;
- log del database;
- informazioni architetturali che confermino la presenza del database.

Nel laboratorio distingueremo:

```text
Fatto osservato
→ deriva direttamente da una evidenza

Ipotesi
→ spiegazione possibile, da verificare

Informazione mancante
→ dato necessario per discriminare le ipotesi
```

## 6. Ruolo dell'LLM nell'incidente

L'LLM non produce i segnali osservabili. Riceve segnali già raccolti e organizzati.

```text
sistema
  ↓
metriche + log + trace + output ML
  ↓
evidence packet
  ↓
LLM
  ↓
sintesi + ipotesi + verifiche
  ↓
validazione umana e tecnica
```

Il suo ruolo è di **assistente all'analisi**, non di autorità finale.

## Domande di controllo

1. In che cosa l'output di un LLM differisce dalla classe prodotta da un Decision Tree?
2. Perché una risposta linguisticamente convincente non costituisce una prova?
3. Che differenza c'è tra addestramento e inferenza?
4. Perché il numero di token è rilevante nell'esecuzione locale?
5. Quale ruolo avrà l'LLM nell'analisi dell'incidente del laboratorio?
