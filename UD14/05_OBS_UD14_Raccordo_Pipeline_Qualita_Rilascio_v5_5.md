# UD14 - Raccordo finale
## Dal deploy automatico alla qualità del rilascio

---

# 1. Cosa abbiamo aggiunto rispetto al primo deploy automatico

Il primo deploy automatico dimostra che una pipeline può portare un'applicazione in cloud.

La UD14 aggiunge un passaggio di qualità:

```text
non solo deploy,
ma deploy separato in fasi e verificato automaticamente.
```

La differenza è sostanziale.

---

# 2. Il nuovo modello operativo

Il modello costruito è:

```text
ValidateRepository
  -> BuildAndPush
  -> DeployToACI
  -> SmokeTest
  -> Evidence
```

Ogni fase ha una responsabilità precisa.

| Fase | Domanda a cui risponde |
|---|---|
| ValidateRepository | il repository contiene ciò che serve? |
| BuildAndPush | l'immagine è stata costruita e pubblicata? |
| DeployToACI | il container cloud è stato creato? |
| SmokeTest | l'applicazione risponde davvero? |
| Evidence | posso dimostrare cosa è successo? |

---

# 3. Perché questo è importante

Una pipeline più leggibile permette di diagnosticare meglio.

Se qualcosa fallisce, non dobbiamo dire genericamente:

```text
la pipeline non funziona
```

Dobbiamo poter dire:

```text
è fallita la validazione
è fallita la build
è fallito il push
è fallito il deploy
è fallito lo smoke test
```

Questa distinzione cambia il modo di lavorare.

---

# 4. Cosa deve restare chiaro

Alla fine della UD14 dobbiamo distinguere:

| Concetto | Significato |
|---|---|
| repository | contiene codice e YAML |
| pipeline | esegue il processo automatico |
| immagine | risultato della build |
| ACR | conserva le immagini |
| ACI | esegue il container cloud |
| smoke test | verifica che l'app risponda |
| log | permettono di capire il comportamento runtime |

---

# 5. Limite consapevole della UD14

La UD14 resta volutamente semplice.

Non stiamo ancora gestendo:

- sistemi con più componenti;
- ambienti multipli;
- approvazioni manuali;
- rollback strutturato;
- osservabilità applicativa avanzata.

Il valore della UD14 è consolidare la qualità minima di una pipeline:

```text
separo,
traccio,
distribuisco,
verifico,
documento.
```

---

# 6. Frase di sintesi

La sintesi della UD14 è:

```text
Una pipeline non deve solo eseguire comandi.
Deve rendere il rilascio leggibile, controllabile e verificabile.
```
