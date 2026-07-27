# LAB guidato — Analisi di un incidente con un LLM

## Durata indicativa

120 minuti.

## Obiettivo

Usare Python e Ollama per analizzare un evidence packet con due prompt differenti, quindi verificare manualmente le affermazioni prodotte.

Questa è l’attività centrale della UD30.

---

## Scenario

Usare:

```text
evidence/incident_catalogo_guidato.md
```

Lo scenario è volutamente incompleto. L’obiettivo non è indovinare una root cause preparata dal docente, ma formulare ipotesi compatibili con i dati e proporre verifiche.

---

## Task 1 — Preparare la baseline umana

Prima di eseguire lo script compilare:

| Elemento | Risposta iniziale |
|---|---|
| Fatti principali | |
| Componente lento nel trace | |
| Ipotesi più plausibile | |
| Ipotesi alternativa | |
| Informazioni mancanti | |
| Prima verifica da eseguire | |

Questa baseline serve a confrontare il proprio ragionamento con il testo generato.

---

## Task 2 — Leggere i due prompt

Aprire:

```text
prompts/prompt_aperto.txt
prompts/prompt_vincolato.txt
```

Individuare nel prompt vincolato:

- vincolo sulle evidenze;
- struttura dell’output;
- richiesta di dichiarare l’incertezza;
- richiesta di verifiche successive.

Non modificare ancora i prompt.

---

## Task 3 — Leggere lo script

Aprire:

```text
scripts/02_compare_prompts.py
```

Lo script:

1. legge l’evidence packet;
2. legge i due template di prompt;
3. inserisce le evidenze nel segnaposto;
4. esegue due chiamate indipendenti;
5. salva le risposte in `runtime/responses`;
6. stampa i metadati principali.

Le chiamate sono indipendenti: il secondo prompt non eredita la conversazione del primo.

---

## Task 4 — Eseguire

```bash
python3 scripts/02_compare_prompts.py
```

Controllare i file creati nella cartella:

```text
runtime/responses/
```

Se Ollama non è disponibile, copiare e usare i file equivalenti in `fallback/risposte_confronto`.

---

## Task 5 — Analizzare il prompt aperto

Usare `templates/matrice_claim_evidence.md`.

Selezionare almeno cinque claim dalla risposta aperta.

Per ciascuno indicare:

- testo del claim;
- evidenza disponibile;
- classificazione;
- verifica necessaria.

Classificazioni ammesse:

```text
FATTO
INTERPRETAZIONE SUPPORTATA
IPOTESI
NON SUPPORTATO
```

### Esempio

| Claim | Evidenza | Classificazione | Verifica |
|---|---|---|---|
| Il p95 è aumentato | metrica 420 → 1.840 ms | FATTO | nessuna |
| La release contiene una query inefficiente | correlazione temporale + trace DB lento | IPOTESI | confronto query e rollback |
| La CPU è satura | metrica CPU assente | NON SUPPORTATO | acquisire CPU DB |

---

## Task 6 — Analizzare il prompt vincolato

Ripetere la valutazione su almeno cinque claim della risposta vincolata.

### Domande

1. La struttura richiesta è rispettata?
2. Le ipotesi sono collegate alle evidenze?
3. Le informazioni mancanti sono dichiarate?
4. Sono ancora presenti claim non supportati?
5. Le verifiche sono tecnicamente eseguibili?

---

## Task 7 — Confrontare la baseline umana

Confrontare la propria analisi iniziale con entrambe le risposte.

| Aspetto | Baseline umana | Prompt aperto | Prompt vincolato |
|---|---|---|---|
| Ipotesi principale | | | |
| Dati mancanti | | | |
| Verifica prioritaria | | | |
| Livello di certezza | | | |

### Attenzione

Una differenza non indica automaticamente che l’AI o la persona abbiano torto. Occorre tornare alle evidenze.

---

## Task 8 — Costruire un evidence packet migliore

L’evidence packet originale è già strutturato, ma può essere migliorato.

Indicare quali dati aggiungere per distinguere tra:

- regressione applicativa;
- query inefficiente;
- saturazione del database;
- problema di rete;
- coincidenza temporale con la release.

Esempi di dati possibili:

- confronto trace prima/dopo;
- metriche CPU e memoria database;
- pool connessioni;
- query e piani di esecuzione;
- esito di rollback o canary;
- latenza di rete;
- distribuzione degli errori per endpoint.

Non aggiungere questi dati come se fossero già disponibili. Inserirli nella sezione `informazioni da acquisire`.

---

## Task 9 — Preparare l’handoff verificabile

Usare:

```text
templates/handoff_verificabile.md
```

L’handoff deve contenere:

1. sintomi osservati;
2. fatti principali;
3. ipotesi più plausibile;
4. evidenze a supporto;
5. ipotesi alternative;
6. informazioni mancanti;
7. verifiche ordinate;
8. livello di certezza;
9. contributo dell’AI e correzioni umane.

### Regola

Non inserire una root cause certa se non è dimostrata dall’evidence packet.

---

## Task 10 — Revisione tra pari

Scambiare l’handoff con un altro partecipante.

Il revisore verifica:

- ogni fatto ha una fonte?
- le ipotesi sono dichiarate?
- il livello di certezza è coerente?
- le verifiche possono confermare o smentire l’ipotesi?
- sono presenti affermazioni introdotte dal modello senza supporto?

Correggere il documento dopo la revisione.

---

## Risultato finale

Il laboratorio non produce “la risposta dell’AI”. Produce:

```text
risposta AI
+ claim–evidence mapping
+ correzione umana
+ handoff verificabile
```

Questa è la competenza professionale trasferibile.
