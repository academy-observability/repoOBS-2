# LP01 — Attività guidate e consolidamento

Queste attività non richiedono codice.
Servono a verificare che la mappa concettuale sia chiara prima di proseguire.

---

## Attività 1 — Dove appartiene?

Associare ogni elemento alla categoria più corretta.

Elementi:

```text
Decision Tree
LLM
rete neurale
mediana
Transformer
RAG
anomaly detection statistica
```

Categorie:

```text
statistica
Machine Learning
Deep Learning
architettura per modelli linguistici
tecnica di recupero + generazione
```

### Domande

1. Un Decision Tree è Machine Learning?
2. È necessariamente una rete neurale?
3. Un LLM appartiene al Deep Learning?
4. La mediana è Machine Learning?

---

## Attività 2 — Training o inference?

Classificare ogni frase.

### Caso A

```text
Uso 1.000 osservazioni storiche con label per costruire un modello.
```

### Caso B

```text
Passo una nuova osservazione al modello già costruito e ottengo anomaly.
```

### Caso C

```text
Confronto le prediction con una reference separata.
```

Scegliere tra:

```text
training
inference
evaluation
```

---

## Attività 3 — È Machine Learning?

Per ogni caso rispondere sì/no e motivare.

### Caso 1

```text
threshold = median + 4 × MAD
```

### Caso 2

```text
un modello costruisce separazioni a partire da esempi già classificati
```

### Caso 3

```text
un LLM genera una spiegazione a partire da prompt e contesto
```

Domanda finale:

> Tutto ciò che chiamiamo “AI” funziona allo stesso modo?

---

## Attività 4 — Correggere le frasi sbagliate

### Frase A

> Un Decision Tree è una piccola rete neurale.

### Frase B

> Deep Learning e Machine Learning sono sinonimi.

### Frase C

> Un LLM recupera sempre la risposta corretta da un database interno.

### Frase D

> RAG significa riaddestrare l’LLM sui documenti aziendali ogni volta che facciamo una domanda.

### Frase E

> Se un LLM produce una risposta molto convincente, possiamo considerarla evidenza.

Riscrivere ogni frase in modo corretto.

---

## Attività 5 — Tre strumenti, tre risultati

Scenario:

```text
Il frontend mostra un p95 elevato.
Abbiamo metriche, alcuni trace e osservazioni storiche validate.
```

Completare:

### Con statistica posso...

```text
________________________________________
```

### Con Machine Learning posso...

```text
________________________________________
```

### Con un LLM posso...

```text
________________________________________
```

### Ma nessuno dei tre, da solo, mi garantisce...

```text
________________________________________
```

---

## Attività 6 — Token, prompt, contesto

Associare:

```text
PROMPT
CONTESTO
TOKEN
```

alle definizioni:

A. Informazioni disponibili al modello durante la richiesta.

B. Unità in cui il testo viene elaborato dal modello.

C. Istruzione o domanda rivolta al modello.

---

## Attività 7 — RAG in un minuto

Consideriamo tre documenti:

```text
A — architettura del Catalogo prodotti
B — runbook operativo
C — trace di una richiesta lenta
```

Domanda:

```text
"Quali componenti attraversa la richiesta lenta?"
```

Un sistema RAG potrebbe:

1. cercare i documenti più pertinenti;
2. recuperare A e C;
3. inserirne parti nel contesto;
4. chiedere all’LLM di rispondere.

### Domanda

Il modello è stato necessariamente riaddestrato?

```text
SÌ / NO
```

Spiegare in una frase.

---

## Attività 8 — Exit ticket

Completare senza consultare gli appunti.

```text
1. Un Decision Tree è ________________________________________

2. Una rete neurale è ________________________________________

3. Deep Learning è ___________________________________________

4. Un LLM è _________________________________________________

5. Training significa ________________________________________

6. Inference significa _______________________________________

7. RAG aggiunge ______________________________________________

8. Una risposta AI non è automaticamente _____________________
```

Se almeno due risposte restano incerte, tornare alla mappa del file `01_LP01_Mappe_ed_Esempi_Visuali.md` prima di iniziare UD28.
