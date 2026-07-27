# LAB guidato — Confronto tra assistente cloud e Ollama Chat

## Durata

90 minuti.

## Obiettivo

Eseguire lo stesso compito con:

- un assistente cloud disponibile;
- un modello locale tramite Ollama Windows, comandato da WSL;

quindi confrontare le risposte rispetto alle evidenze.

## Prerequisiti

- setup e preflight completati;
- `OLLAMA_MODEL` configurato;
- accesso a un assistente cloud oppure fallback;
- dati sintetici della UD.

## Task 1 — Preparare la scheda

Copiare:

```bash
cp templates/scheda_confronto_assistenti.md outputs/scheda_confronto_assistenti.md
```

Registrare:

- data e ora;
- prodotto cloud e modalità visibile;
- strumenti attivi;
- modello Ollama;
- endpoint configurato, senza riportare informazioni sensibili.

## Task 2 — Baseline umana

Leggere:

```text
evidence/incident_catalogo_guidato.md
```

Senza usare l'LLM, annotare:

1. tre fatti;
2. componente che contribuisce maggiormente alla durata del trace;
3. informazioni mancanti;
4. una ipotesi, marcata chiaramente come tale.

## Task 3 — Prompt aperto nel cloud

Usare `prompts/prompt_aperto.txt`, aggiungendo l'evidence packet.

Salvare la risposta in:

```text
outputs/cloud_prompt_aperto.md
```

## Task 4 — Stesso prompt in Ollama Chat

Da WSL:

```bash
ollama.exe run "$OLLAMA_MODEL"
```

Incollare lo stesso prompt e lo stesso evidence packet.

Salvare la risposta in:

```text
outputs/ollama_prompt_aperto.md
```

Uscire con `/bye`.

## Task 5 — Applicare la griglia

| Criterio | Cloud | Ollama | Evidenza del giudizio |
|---|---|---|---|
| separa fatti e ipotesi | | | |
| cita dati disponibili | | | |
| dichiara informazioni mancanti | | | |
| evita cause certe | | | |
| propone verifiche | | | |
| introduce dettagli assenti | | | |

Usare `Sì`, `Parzialmente`, `No`.

## Task 6 — Prompt vincolato

Aprire nuove conversazioni e usare:

```text
prompts/prompt_vincolato.txt
```

Salvare:

```text
outputs/cloud_prompt_vincolato.md
outputs/ollama_prompt_vincolato.md
```

## Task 7 — Confrontare

| Sistema | Prompt | Fatti | Ipotesi | Mancanze | Verifiche | Claim non supportati |
|---|---|---:|---:|---:|---:|---:|
| Cloud | aperto | | | | | |
| Cloud | vincolato | | | | | |
| Ollama | aperto | | | | | |
| Ollama | vincolato | | | | | |

## Conclusione

```text
stesso evidence packet + stesso prompt
≠ risposta identica
```

```text
risposta convincente
≠ causa dimostrata
```

In caso di indisponibilità usare `fallback/risposte_confronto/`.
