# LAB autonomo — Handoff di un incidente con supporto LLM

## Durata

90 minuti.

## Obiettivo

Produrre un handoff tecnico verificabile, senza delegare la decisione finale all'LLM.

## Scenario

Usare:

```text
evidence/incident_checkout_autonomo.md
```

## Task 1 — Lettura umana

Compilare:

- fatti osservati;
- inferenze possibili;
- informazioni mancanti;
- almeno due ipotesi concorrenti.

## Task 2 — Interrogazione LLM

Usare:

```text
prompts/prompt_autonomo_handoff.txt
```

È ammesso:

- assistente cloud autorizzato;
- Ollama locale;
- fallback predisposto.

Registrare prodotto/modello e data.

## Task 3 — Validare la risposta

Per ogni claim importante indicare:

- ID delle evidenze;
- categoria;
- supportato/non supportato;
- correzione necessaria.

## Task 4 — Produrre l'handoff finale

Copiare:

```bash
cp templates/handoff_incidente.md outputs/handoff_checkout_autonomo.md
```

Il file finale deve contenere:

1. sintesi esecutiva;
2. fatti con ID;
3. ipotesi ordinate;
4. informazioni mancanti;
5. verifiche consigliate;
6. azioni immediate a basso rischio;
7. claim dell'LLM scartati o corretti;
8. livello di confidenza motivato.

## Task 5 — Nota di metodo

Rispondere:

1. Quale parte dell'handoff è stata migliorata dall'LLM?
2. Quale claim richiedeva correzione?
3. Quale verifica è stata scelta e perché?
4. Che cosa non può essere concluso dai dati disponibili?

## Criteri di completamento

- [ ] baseline umana presente;
- [ ] evidence packet rispettato;
- [ ] fatti e ipotesi separati;
- [ ] claim collegati agli ID;
- [ ] almeno un claim non supportato rilevato oppure motivata la sua assenza;
- [ ] verifiche concrete e ordinate;
- [ ] nessuna root cause presentata come certa senza prova;
- [ ] handoff finale leggibile.
