# UD13 - Mini-attività
## Mappa del flusso pipeline, ACR e ACI

---

# Obiettivo

Ricostruire con parole proprie il flusso realizzato nel laboratorio guidato.

Non è richiesto memorizzare una sequenza di unità didattiche successive. L'obiettivo è capire la catena tecnica della UD13.

---

# Attività 1 - Completa la mappa

Completa la mappa inserendo il ruolo di ogni elemento:

```text
GitHub
  -> Azure DevOps Pipeline
  -> docker build
  -> Azure Container Registry
  -> Azure Container Instances
  -> curl
  -> az container logs
```

Per ogni elemento scrivi una frase breve:

| Elemento | Ruolo nel flusso |
|---|---|
| GitHub | |
| Azure DevOps Pipeline | |
| `docker build` | |
| ACR | |
| ACI | |
| `curl` | |
| `az container logs` | |

---

# Attività 2 - Domande di consolidamento

Rispondi in modo asciutto ma chiaro.

1. Dove vive il codice sorgente?
2. Dove gira la pipeline?
3. Dove viene costruita l'immagine Docker?
4. Dove viene salvata l'immagine?
5. Dove gira il container finale?
6. Perché serve un tag immagine?
7. Perché `Build.BuildId` è utile?
8. Che differenza c'è tra `docker logs` e `az container logs`?
9. Perché il deploy automatico è più tracciabile di un deploy manuale?
10. Quale comando permette di vedere i tag dell'immagine in ACR?

---

# Output atteso

Aggiungi la risposta nel file evidenze:

```text
docs/evidence_ud13.md
```
