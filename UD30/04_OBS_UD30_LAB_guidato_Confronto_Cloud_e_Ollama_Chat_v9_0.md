# LAB guidato — Confronto tra assistente cloud e Ollama Chat

## Durata indicativa

90 minuti.

## Obiettivo

Eseguire lo stesso compito con:

- un assistente cloud disponibile tra ChatGPT, Gemini e Claude;
- un modello locale tramite Ollama Chat;

quindi confrontare le risposte con criteri verificabili.

Il laboratorio non stabilisce quale prodotto sia “migliore”. Mostra che sistemi diversi possono produrre analisi diverse e che ogni risposta deve essere verificata rispetto alle evidenze.

---

## Prerequisiti

- aver letto i file teorici `00` e `01`;
- aver completato `09A_OBS_UD30_Preflight_Compatibilita_e_Prima_Chat_Ollama_WSL_v9_0.md`;
- avere accesso ad almeno un assistente cloud oppure usare le risposte di fallback;
- avere Ollama avviato con almeno un modello locale;
- usare esclusivamente i dati sintetici forniti.

---

## Scenario

Il Catalogo prodotti mostra un degrado improvviso. L’evidence packet si trova in:

```text
evidence/incident_catalogo_guidato.md
```

Non aggiungere dati esterni. Non cercare una soluzione su Internet.

---

## Task 1 — Preparare un confronto controllato

Aprire `templates/scheda_confronto_assistenti.md`.

Registrare:

- data e ora della prova;
- servizio usato;
- modello o modalità mostrata dall’interfaccia, se disponibile;
- tipo di account, solo come `free`, `paid` o `unknown`;
- strumenti attivi;
- nome del modello Ollama.

### Perché è necessario

Una risposta non può essere attribuita genericamente a “ChatGPT” o “Gemini” senza registrare almeno ciò che l’interfaccia rende visibile. Le modalità disponibili possono dipendere dal piano e cambiare nel tempo.

---

## Task 2 — Leggere le evidenze prima dell’AI

Leggere l’evidence packet e rispondere senza usare un LLM:

1. Quali sono tre fatti direttamente osservati?
2. Quale componente contribuisce maggiormente alla latenza nel trace disponibile?
3. La nuova release è certamente la causa? Perché?
4. Quali informazioni mancano?

Annotare le risposte nella scheda.

### Risultato atteso

Il partecipante deve possedere una valutazione iniziale prima di leggere il testo generato. In caso contrario, la risposta dell’AI diventerebbe il punto di partenza incontrollato.

---

## Task 3 — Eseguire il prompt aperto sul servizio cloud

Aprire una nuova conversazione nell’assistente assegnato.

Quando possibile:

- disattivare ricerca web;
- non allegare altri file;
- non usare una conversazione precedente;
- non chiedere una seconda risposta.

Copiare il contenuto di:

```text
prompts/prompt_aperto.txt
```

sostituendo il segnaposto con l’evidence packet.

Salvare la risposta nella scheda oppure in un file locale.

### Domande

- Il sistema presenta una causa come certa?
- Quali affermazioni non compaiono nell’evidence packet?
- Indica esplicitamente ciò che manca?
- Propone verifiche o soltanto una conclusione?

---

## Task 4 — Eseguire lo stesso prompt con Ollama Chat

Nel terminale:

```bash
ollama run llama3.2:1b
```

Se il modello di riferimento non è eseguibile:

```bash
ollama run gemma3:1b
```

`gemma3:270m` è un fallback estremo: usarlo soltanto per completare la prova tecnica. Per il confronto qualitativo utilizzare gli output predisposti, perché un modello così piccolo può non seguire adeguatamente il prompt.

Incollare esattamente lo stesso prompt usato nel Task 3.

Per terminare la sessione usare:

```text
/bye
```

Registrare il nome esatto del modello.

### Domande

- La risposta locale è più breve o più lunga?
- Segue la richiesta?
- Introduce informazioni non fornite?
- Distingue correlazione e causalità?

Non valutare il modello soltanto dalla fluidità dell’italiano.

---

## Task 5 — Applicare la griglia

Valutare entrambe le risposte usando:

| Criterio | Cloud | Ollama | Evidenza del giudizio |
|---|---|---|---|
| Distingue fatti e ipotesi | | | |
| Cita i dati disponibili | | | |
| Dichiara le informazioni mancanti | | | |
| Evita cause certe non dimostrate | | | |
| Propone verifiche successive | | | |
| Introduce dettagli non forniti | | | |

Usare valori:

```text
Sì / Parzialmente / No
```

Nell’ultima colonna riportare una frase breve della risposta, non un’impressione generica.

---

## Task 6 — Eseguire il prompt vincolato

Aprire una nuova conversazione cloud e una nuova sessione Ollama. Non continuare le conversazioni precedenti: la cronologia modificherebbe il contesto.

Usare:

```text
prompts/prompt_vincolato.txt
```

Eseguire prima sul servizio cloud e poi in Ollama Chat.

---

## Task 7 — Confrontare aperto e vincolato

Compilare:

| Sistema | Prompt | Fatti separati | Ipotesi dichiarate | Dati mancanti | Verifiche | Claim non supportati |
|---|---|---:|---:|---:|---:|---:|
| Cloud | aperto | | | | | |
| Cloud | vincolato | | | | | |
| Ollama | aperto | | | | | |
| Ollama | vincolato | | | | | |

### Domanda centrale

Il prompt vincolato ha reso la risposta:

- più corretta;
- più strutturata;
- più verificabile;
- oppure tutte e tre?

La risposta attesa non è automatica. È possibile che migliori la struttura senza eliminare tutti i claim non supportati.

---

## Task 8 — Discussione tra gruppi

Ogni gruppo presenta:

1. un punto di forza della risposta cloud;
2. un punto di forza della risposta locale;
3. un claim non supportato trovato;
4. una verifica utile proposta;
5. un limite del confronto.

Se i gruppi hanno usato ChatGPT, Gemini e Claude differenti, confrontare i risultati senza trasformarli in una classifica commerciale.

---

## Conclusione

Il laboratorio deve far emergere che:

```text
stesso evidence packet
+ stesso prompt
≠ risposta identica
```

ma soprattutto:

```text
risposta convincente
≠ causa dimostrata
```

Il prompt vincolato è utile perché rende più visibili fatti, ipotesi, limiti e verifiche. La responsabilità della validazione resta all’operatore.

---

## Continuità didattica

Se un servizio cloud o Ollama non è disponibile, usare i file nella cartella:

```text
fallback/risposte_confronto/
```

Il partecipante svolge comunque Task 5–8.
