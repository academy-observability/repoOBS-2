# OBS UD11 - DevOps, Azure DevOps e architettura del flusso CI/CD cloud

Versione: v5.5.1  
Destinatari: partecipanti

---

# Scopo della UD11

UD11 apre la parte DevOps del percorso Observability.

La UD non introduce ancora Docker operativo, ACR, ACI o Azure Container Apps in modalità pratica.

UD11 serve a costruire la base:

```text
DevOps
CI/CD
Pipeline
GitHub come repository codice
Azure DevOps come motore CI/CD
ACR come registry immagini
Azure come target di deploy
Observability come verifica post-deploy
```

---

# Sequenza consigliata di studio ed esecuzione

Segui i file in questo ordine.

| Ordine | File | Quando usarlo | Output atteso |
|---:|---|---|---|
| 1 | `00_OBS_UD11_Concetti_DevOps_AzureDevOps_Flusso_v5_5.md` | Prima parte teorica guidata | Comprendere DevOps, CI/CD, pipeline, repository, artifact, registry e deploy |
| 2 | `01_OBS_UD11_LAB_guidato_Setup_Azure_DevOps_Organizzazione_Progetto_v5_5.md` | Laboratorio guidato | Organizzazione Azure DevOps e progetto `Observability-DevOps` creati o verificati |
| 3 | `04_OBS_UD11_GUIDA_OPERATIVA_AzureDevOps_Passo_Passo_v5_5.md` | Supporto durante il laboratorio guidato | Riferimento rapido per ritrovare schermate, sezioni e controlli principali |
| 4 | `02_OBS_UD11_MINI_ATTIVITA_Mappa_Flusso_DevOps_Cloud_v5_5.md` | Dopo il laboratorio guidato | File `docs/evidence_ud11_mappa_flusso.md` compilato |
| 5 | `03_OBS_UD11_LAB_autonomo_Verifica_Prerequisiti_AzureDevOps_v5_5.md` | Attività autonoma pomeridiana | File di evidenza autonomo compilato e prerequisiti verificati |


Nota importante: la sequenza sopra è la sequenza di lavoro **della UD11**.  
Non è una pianificazione rigida delle UD successive.

---

# File principali

| File | Uso |
|---|---|
| `00_OBS_UD11_Concetti_DevOps_AzureDevOps_Flusso_v5_5.md` | Concetti base della UD11 |
| `01_OBS_UD11_LAB_guidato_Setup_Azure_DevOps_Organizzazione_Progetto_v5_5.md` | Laboratorio guidato setup Azure DevOps |
| `02_OBS_UD11_MINI_ATTIVITA_Mappa_Flusso_DevOps_Cloud_v5_5.md` | Mini-attività sulla mappa del flusso |
| `03_OBS_UD11_LAB_autonomo_Verifica_Prerequisiti_AzureDevOps_v5_5.md` | Laboratorio autonomo pomeridiano |
| `04_OBS_UD11_GUIDA_OPERATIVA_AzureDevOps_Passo_Passo_v5_5.md` | Guida rapida operativa |
| `05_OBS_UD11_GUIDA_PROSSIME_UD_Docker_ACR_ACI_ACA_v5_5.md` | Raccordo concettuale con i temi tecnici successivi |

---

# Cartelle

| Cartella | Uso |
|---|---|
| `docs/` | File compilati dai partecipanti |
| `evidence/` | Screenshot ed evidenze operative |
| `img/` | Immagini opzionali |
| `config/` | Note configurative non segrete |

---

# Output atteso della UD11

Alla fine della UD11 il partecipante deve avere:

- organizzazione Azure DevOps creata o verificata;
- progetto `Observability-DevOps` creato o verificato;
- accesso a Pipelines verificato;
- accesso a Project settings verificato;
- sezione Service connections individuata;
- file di evidenza compilati in `docs/`;
- mappa concettuale generale del flusso DevOps cloud chiara.

---

# Cosa NON si fa in UD11

In UD11 non si eseguono ancora:

```bash
docker build
docker run
docker push
```

In UD11 non si crea ancora un deploy automatico su Azure.

Questi argomenti richiedono prima una base Docker e poi una pipeline operativa.

