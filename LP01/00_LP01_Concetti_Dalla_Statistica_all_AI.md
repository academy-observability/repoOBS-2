# LP01 — Concetti
# Dalla statistica all’AI: costruire la mappa prima dei dettagli

## 1. Da dove partiamo

In UD27 abbiamo imparato a descrivere dati osservabili:

```text
osservazioni
→ dataset
→ selezione
→ gruppi
→ media / mediana / p95
→ descrizione del comportamento
```

Ora serve una mappa per capire che cosa succede quando, oltre a **descrivere**, vogliamo:

- riconoscere scostamenti;
- apprendere da esempi passati;
- ottenere supporto nella formulazione di ipotesi.

Questi obiettivi non richiedono tutti lo stesso tipo di tecnica.

---

## 2. Tre modi diversi di usare i dati

### A. Statistica e regole definite da noi

Possiamo descrivere un comportamento e definire un criterio.

Esempio concettuale:

```text
comportamento storico
→ costruisco un riferimento
→ confronto nuove osservazioni
→ segnalo uno scostamento
```

Qui la logica generale del criterio è decisa da noi.

Questo prepara il terreno a ciò che verrà affrontato operativamente in UD28.

### B. Machine Learning

Nel Machine Learning forniamo dati e, a seconda del problema, esempi o segnali dai quali un algoritmo costruisce un modello.

Schema minimo:

```text
esempi
+ informazioni disponibili
        ↓
     training
        ↓
      modello
        ↓
nuove osservazioni
        ↓
    prediction
```

L’idea importante è:

> il comportamento del modello non viene scritto regola per regola nel codice applicativo.

In UD29 vedremo concretamente questo passaggio con un modello semplice e leggibile.

### C. AI generativa / LLM

Un LLM riceve testo e contesto e produce nuovo testo.

Può aiutarci a:

- riassumere evidenze;
- organizzare informazioni;
- proporre ipotesi;
- suggerire verifiche.

Ma il testo generato non diventa automaticamente una verità tecnica.

Questo sarà il centro di UD30.

---

## 3. La mappa: AI, Machine Learning, reti neurali, LLM

```text
ARTIFICIAL INTELLIGENCE
        │
        └── MACHINE LEARNING
                │
                ├── algoritmi come Decision Tree
                │
                └── NEURAL NETWORKS
                        │
                        └── DEEP LEARNING
                                │
                                └── TRANSFORMER
                                        │
                                        └── LLM
```

Questa è una **mappa concettuale**, non una classificazione completa di tutta l’AI.
Serve a collocare gli strumenti che incontreremo nel corso.

### Da ricordare

```text
Decision Tree
→ Machine Learning
→ NON è una rete neurale
```

```text
LLM
→ Machine Learning
→ Deep Learning
→ rete neurale di grande scala
→ tipicamente basato su architettura Transformer
```

---

## 4. Machine Learning: che cosa significa “apprendere”

Confrontiamo due schemi.

### Programma tradizionale

```text
dati
+
regole scritte da noi
        ↓
      output
```

### Machine Learning supervisionato

```text
esempi
+
risposte note
        ↓
      training
        ↓
      modello
        ↓
nuovi dati
        ↓
    prediction
```

Tre parole che incontreremo:

### Training

È la fase in cui il modello viene costruito o adattato usando i dati disponibili.

### Inference

È la fase in cui il modello già costruito viene applicato a nuovi dati.

### Evaluation

È il momento in cui verifichiamo quanto bene il modello si comporta rispetto a un riferimento.

In questa lezione ci basta capire la differenza.
In UD29 la vedremo concretamente.

---

## 5. Supervisionato e non supervisionato

### Apprendimento supervisionato

Abbiamo esempi con una risposta di riferimento.

```text
osservazione 1 → normal
osservazione 2 → anomaly
osservazione 3 → normal
```

Il modello può usare questi esempi durante il training.

### Apprendimento non supervisionato

Non forniamo una risposta corretta per ogni esempio.
Cerchiamo invece strutture, gruppi o comportamenti insoliti nei dati.

```text
dati
→ struttura / distanza / deviazione
→ possibili gruppi o anomalie
```

### Importante

```text
anomaly detection
≠ sempre Machine Learning
```

È possibile rilevare anomalie anche con metodi statistici definiti esplicitamente.

Questo evita una confusione importante prima di UD28 e UD29.

---

## 6. Che cos’è una rete neurale

Una rete neurale è un tipo di modello composto da unità interconnesse organizzate in livelli.

Schema intuitivo:

```text
INPUT
│
├── duration_ms
├── status_code
└── error_rate
        ↓
      ○ ○ ○ ○
        ↓
      ○ ○ ○
        ↓
       ○ ○
        ↓
      OUTPUT
```

Durante il training vengono adattati molti parametri interni.

Non serve, per questo percorso, conoscere:

- la matematica della backpropagation;
- il calcolo delle derivate;
- TensorFlow o PyTorch;
- la programmazione di una rete neurale.

Serve soltanto capire che:

> una rete neurale è un modo diverso, e spesso molto più complesso, di costruire un modello che apprende dai dati.

---

## 7. Deep Learning

Quando reti neurali con molti livelli e moltissimi parametri vengono utilizzate per apprendere rappresentazioni complesse, parliamo di **Deep Learning**.

Schema:

```text
Machine Learning
        │
        ├── Decision Tree
        │
        └── Neural Networks
                │
                └── Deep Learning
```

Non tutto il Machine Learning è Deep Learning.

```text
Decision Tree
→ ML
→ non Deep Learning
```

```text
LLM moderno
→ ML
→ Deep Learning
```

---

## 8. Dal testo ai token

Un modello linguistico non riceve il testo esattamente come lo leggiamo noi.

In modo semplificato:

```text
"Il frontend è lento"
        ↓
       token
        ↓
rappresentazioni numeriche
        ↓
      modello
```

Un **token** è una unità in cui il testo viene suddiviso per essere elaborato dal modello.

Non dobbiamo conoscere l’algoritmo di tokenizzazione.
Ci basta capire perché, nei sistemi AI, incontreremo misure come:

```text
input_tokens
output_tokens
```

---

## 9. Transformer: il concetto essenziale

I moderni LLM usati comunemente sono tipicamente basati su architetture Transformer.

Per questa lezione ci basta una sola idea:

> il Transformer è progettato per elaborare sequenze e mettere in relazione elementi del contesto in modo efficace.

Schema semplificato:

```text
testo
→ token
→ Transformer
→ relazioni nel contesto
→ rappresentazioni
→ generazione
```

Non approfondiamo:

- query/key/value;
- multi-head attention;
- matrici;
- positional encoding matematico.

Questi dettagli non sono necessari per utilizzare correttamente un LLM nell’Observability.

---

## 10. Che cos’è un LLM

LLM significa **Large Language Model**.

È un grande modello di Deep Learning addestrato su enormi quantità di testo per modellare e generare linguaggio.

Dal punto di vista dell’utilizzatore:

```text
prompt
+
contesto
        ↓
       LLM
        ↓
testo generato
```

Può produrre una risposta molto convincente.
Ma:

```text
risposta plausibile
≠
risposta dimostrata
```

Un LLM non deve essere pensato come:

```text
un database che restituisce sempre la risposta corretta
```

È un modello generativo.

---

## 11. Perché può generare affermazioni non supportate

Supponiamo di avere queste informazioni:

```text
frontend più lento del backend
un trace lento
nessun database applicativo nello scenario
```

Un LLM potrebbe comunque produrre una frase come:

```text
"Il database è probabilmente saturo."
```

La frase può sembrare tecnicamente plausibile in astratto, ma nel nostro scenario non è supportata.

La domanda corretta diventa:

> Quale evidenza dimostra questa affermazione?

Questa idea prepara direttamente UD30.

---

## 12. Prompt e contesto

### Prompt

È l’istruzione o la richiesta che diamo al modello.

### Contesto

È l’insieme delle informazioni disponibili al modello mentre genera la risposta.

Schema:

```text
PROMPT
"Analizza queste evidenze"
        +
CONTESTO
metriche / trace / architettura
        ↓
       LLM
        ↓
     risposta
```

La qualità del prompt e del contesto influenza la risposta.
Ma non garantisce automaticamente la correttezza.

---

## 13. RAG: solo il concetto

RAG significa **Retrieval-Augmented Generation**.

Serve a combinare un LLM con un meccanismo che recupera informazioni pertinenti prima della generazione.

```text
domanda
→ ricerca informazioni rilevanti
→ documenti / frammenti recuperati
→ aggiunti al contesto
→ LLM
→ risposta
```

### Da non confondere

```text
RAG
≠
riaddestrare il modello
```

RAG modifica il **contesto disponibile durante la richiesta**, non necessariamente i parametri del modello.

Nel nostro percorso non costruiremo un sistema RAG.
Il concetto serve soltanto a orientarsi nel lessico AI moderno.

---

## 14. Collegamento con Observability

La stessa telemetria può essere utilizzata con approcci diversi.

```text
METRICHE / LOG / TRACE
        │
        ├── statistica
        │      ↓
        │   descrizione / baseline / scostamento
        │
        ├── Machine Learning
        │      ↓
        │   modello / prediction
        │
        └── LLM
               ↓
            sintesi / ipotesi / verifiche suggerite
```

I tre risultati non sono equivalenti.

```text
candidate statistica
≠ prediction ML
≠ risposta generativa
```

E nessuno dei tre equivale automaticamente a:

```text
root cause accertata
```

---

## 15. La mappa da portare con sé

```text
UD27
so descrivere i dati
        ↓
LP01
capisco la mappa dei metodi
        ↓
UD28
uso statistica per baseline e anomaly detection
        ↓
UD29
vedo un modello ML apprendere dagli esempi
        ↓
UD30
uso un LLM reale e verifico ciò che produce
```

Questa lezione serve a orientarsi.
Le UD successive serviranno a fare esperienza concreta dei singoli passaggi.
