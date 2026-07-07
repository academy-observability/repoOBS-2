# OBS UD11 - Laboratorio autonomo
## Verifica prerequisiti Azure DevOps e decision record iniziale

Versione: v5.5  
Destinatari: partecipanti  
Durata consigliata: 2 ore  
Tipo attività: laboratorio autonomo

---

# 1. Obiettivo

In questo laboratorio autonomo devi verificare in modo indipendente che il tuo ambiente sia pronto per le prossime UD.

Non devi creare pipeline, immagini o deploy.

Devi produrre un piccolo report tecnico che dimostri di avere capito:

- che cosa hai creato o verificato;
- quali permessi hai;
- dove si trovano le sezioni importanti;
- quali rischi o blocchi potrebbero emergere nelle prossime UD;
- quale decisione operativa prenderesti prima di iniziare con pipeline e deploy.

---

# 2. Scenario

Sei un partecipante del percorso Observability.

Hai già visto risorse Azure in UD05 e hai lavorato su monitoraggio e log nelle UD successive.

Ora il team vuole iniziare una fase DevOps:

```text
GitHub -> Azure DevOps -> ACR -> deploy Azure -> osservabilità
```

Prima di partire, devi verificare che il contenitore Azure DevOps sia pronto.

---

# 3. Task 1 - Verifica accessi

Compila questa tabella.

| Elemento | Valore / esito |
|---|---|
| Account usato per Azure DevOps |  |
| Nome organizzazione Azure DevOps |  |
| URL organizzazione |  |
| Nome progetto |  |
| Riesco ad aprire Pipelines |  |
| Riesco ad aprire Project settings |  |
| Riesco a vedere Service connections |  |
| Account GitHub disponibile |  |
| Subscription Azure nota |  |

---

# 4. Task 2 - Spiega i ruoli

Scrivi una spiegazione breve per ciascun elemento.

## GitHub

```text
...
```

## Azure DevOps Pipelines

```text
...
```

## Azure Container Registry

```text
...
```

## Azure Container Instances

```text
...
```

## Azure Container Apps

```text
...
```

## Application Insights / Azure Monitor / Log Analytics

```text
...
```

---

# 5. Task 3 - Individua i prerequisiti mancanti

Completa la tabella.

| Prerequisito | Disponibile? | Azione necessaria |
|---|---|---|
| Organizzazione Azure DevOps |  |  |
| Progetto Azure DevOps |  |  |
| Accesso a Project settings |  |  |
| Accesso a Pipelines |  |  |
| Account GitHub funzionante |  |  |
| Repository GitHub da usare nelle prossime UD |  |  |
| Subscription Azure individuata |  |  |
| Resource Group del corso individuato |  |  |
| ACR già esistente o da creare in seguito |  |  |

Se un prerequisito non è ancora richiesto in UD11, scrivi:

```text
Non richiesto in UD11, da completare nella UD successiva indicata dal docente.
```

---

# 6. Task 4 - Decision record iniziale

Crea un breve decision record.

Usa questa struttura:

```md
# Decision Record UD11

## Contesto
Il percorso passa da attività Azure manuali a un ciclo DevOps automatizzato.

## Decisione
Useremo GitHub come repository del codice e Azure DevOps Pipelines come motore CI/CD.

## Motivazione
...

## Conseguenze operative
...

## Rischi o prerequisiti da controllare
...
```

---

# 7. Task 5 - Risposta libera

Rispondi alla domanda:

```text
Perché è sbagliato iniziare subito da Docker e dalle pipeline senza avere prima chiarito ruoli, account, progetto e service connection?
```

Risposta:

```text
...
```

---

# 8. File da consegnare

Crea il file:

```bash
code docs/evidence_ud11_lab_autonomo.md
```

Il file deve contenere:

- tabella accessi;
- spiegazione ruoli;
- prerequisiti mancanti;
- decision record;
- risposta libera finale.

---

# 9. Criteri di valutazione

Il docente valuterà soprattutto:

- chiarezza dei ruoli;
- coerenza tra GitHub, Azure DevOps, ACR e Azure;
- capacità di distinguere UD11 dalle UD successive;
- capacità di individuare prerequisiti mancanti;
- qualità del decision record.

Non viene valutata la creazione di una pipeline, perché non è obiettivo della UD11.
