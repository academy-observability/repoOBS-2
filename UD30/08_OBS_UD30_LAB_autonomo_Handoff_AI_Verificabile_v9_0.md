# LAB autonomo — Handoff AI verificabile

## Durata indicativa

60–75 minuti.

## Scenario

Usare:

```text
evidence/incident_checkout_autonomo.md
```

L’incidente riguarda il servizio Checkout. Non riutilizzare automaticamente le conclusioni del laboratorio sul Catalogo prodotti.

---

## Consegna

Produrre una cartella con:

```text
01_baseline_umana.md
02_prompt_usato.txt
03_risposta_llm.md
04_matrice_claim_evidence.md
05_handoff_finale.md
06_telemetria.csv
```

Se Ollama non è disponibile, usare la risposta e la telemetria di fallback indicate nel file scenario.

---

## Task 1 — Baseline umana

Senza AI indicare:

- fatti osservati;
- ipotesi principale;
- almeno un’ipotesi alternativa;
- informazioni mancanti;
- prima verifica.

---

## Task 2 — Preparare il prompt

Costruire un prompt vincolato che richieda:

1. fatti;
2. ipotesi;
3. supporto delle ipotesi;
4. informazioni mancanti;
5. verifiche successive.

Non copiare meccanicamente il prompt guidato: adattarlo al nuovo scenario mantenendo gli stessi principi.

---

## Task 3 — Eseguire l’LLM

Usare il modello disponibile tramite uno degli script forniti oppure una piccola copia adattata di `02_compare_prompts.py`.

Registrare:

- modello;
- timestamp;
- latenza;
- token input/output;
- esito tecnico.

---

## Task 4 — Validare almeno sei claim

Usare le classificazioni:

```text
FATTO
INTERPRETAZIONE SUPPORTATA
IPOTESI
NON SUPPORTATO
```

Ogni claim deve essere collegato a una riga dell’evidence packet oppure dichiarato non supportato.

---

## Task 5 — Preparare l’handoff

L’handoff deve essere utilizzabile da un secondo operatore che non ha partecipato all’analisi.

Deve contenere:

- sintomo e impatto;
- finestra temporale;
- evidenze principali;
- ipotesi prioritaria e livello di certezza;
- ipotesi alternative;
- verifiche ordinate;
- cosa non è ancora noto;
- correzioni apportate alla risposta AI.

---

## Task 6 — Autovalutazione

Attribuire da 0 a 2 punti per ciascun criterio:

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| Aderenza alle evidenze | claim inventati | parziale | completa |
| Fatti/ipotesi | confusi | parzialmente separati | chiaramente separati |
| Dati mancanti | assenti | incompleti | pertinenti |
| Verifiche | generiche | alcune concrete | ordinate e falsificabili |
| Telemetria | assente | incompleta | completa |
| Handoff | ambiguo | utilizzabile con correzioni | professionale |

Punteggio massimo: 12.

---

## Criterio di riuscita

Il laboratorio è riuscito se il partecipante dimostra di saper correggere e vincolare l’output del modello. Non è richiesto che il modello individui la causa reale.
