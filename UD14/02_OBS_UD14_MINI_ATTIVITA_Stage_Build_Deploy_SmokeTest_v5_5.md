# UD14 - Mini-attività
## Ricostruire gli stage della pipeline multistage

---

# 1. Obiettivo

Questa mini-attività serve a verificare che abbiamo capito la separazione tra le fasi della pipeline UD14.

Non basta sapere che la pipeline è riuscita. Dobbiamo saper dire **che cosa è successo in ogni stage**.

---

# 2. Tabella da completare

Completa la tabella.

| Stage | Cosa fa | Output o verifica attesa |
|---|---|---|
| `ValidateRepository` |  |  |
| `BuildAndPush` |  |  |
| `DeployToACI` |  |  |
| `SmokeTest` |  |  |

---

# 3. Domande brevi

Rispondi in modo asciutto ma preciso.

## 3.1 Quale stage verifica la struttura del repository?

Risposta:

```text

```

## 3.2 Quale stage costruisce l'immagine Docker?

Risposta:

```text

```

## 3.3 Quale stage pubblica l'immagine in ACR?

Risposta:

```text

```

## 3.4 Quale stage crea o aggiorna ACI?

Risposta:

```text

```

## 3.5 Quale stage verifica gli endpoint HTTP?

Risposta:

```text

```

## 3.6 Perché `/error` non viene usato nello smoke test bloccante?

Risposta:

```text

```

## 3.7 Perché `Build.BuildId` è utile come tag immagine?

Risposta:

```text

```

## 3.8 Che differenza c'è tra deploy riuscito e applicazione funzionante?

Risposta:

```text

```

## 3.9 Dove si vede il FQDN finale dell'applicazione?

Risposta:

```text

```

## 3.10 Quale comando permette di leggere i log del container cloud?

Risposta:

```text

```

---

# 4. Mini-schema finale

Completa lo schema indicando il ruolo di ogni blocco.

```text
GitHub
  -> Azure DevOps Pipeline
      -> ValidateRepository: ...
      -> BuildAndPush: ...
      -> DeployToACI: ...
      -> SmokeTest: ...
  -> ACR: ...
  -> ACI: ...
```
