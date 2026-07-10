# UD15 - FE/BE, monorepo, multi-image e ACR

## Scopo della UD

In UD15 passiamo da una singola applicazione containerizzata a un piccolo sistema composto da frontend e backend.

L'obiettivo è costruire e pubblicare due immagini Docker distinte in Azure Container Registry tramite Azure DevOps.

## Cosa si fa

- Creazione/verifica progetto FE/BE.
- Build locale di due immagini.
- Test locale frontend -> backend.
- Pipeline Azure DevOps multi-image.
- Push immagini `frontend` e `backend` su ACR.
- Verifica repository e tag in ACR.

## Cosa non si fa

- Non si usa GitHub Actions.
- Non si usa App Service for Containers.
- Non si fa ancora deploy FE/BE su Azure Container Apps.
- Non si introduce ancora Application Insights.

## Sequenza consigliata di studio

1. `00_OBS_UD15_Concetti_FE_BE_Monorepo_MultiImage_ACR_v5_6.md`
2. `07_OBS_UD15_GUIDA_ARCHITETTURA_FE_BE_RETE_CONTAINER_v5_6.md`
3. `04_OBS_UD15_GUIDA_OPERATIVA_FE_BE_Docker_ACR_AzureDevOps_v5_6.md`
4. `01_OBS_UD15_LAB_guidato_FE_BE_Docker_Locale_MultiImage_ACR_v5_6.md`
5. `02_OBS_UD15_MINI_ATTIVITA_Mappa_FE_BE_Immagini_ACR_v5_6.md`
6. `03_OBS_UD15_LAB_autonomo_Nuova_Versione_FE_BE_MultiImage_v5_6.md`
7. `05_OBS_UD15_Raccordo_MultiImage_Deploy_FE_BE_v5_6.md`

## Output atteso

Alla fine della UD15 devi poter mostrare:

- frontend e backend funzionanti localmente in container;
- comunicazione frontend -> backend tramite `BACKEND_URL`;
- spiegazione di rete Docker locale, porte host/container e DNS interno;
- pipeline Azure DevOps eseguita con successo;
- repository `frontend` e `backend` presenti in ACR;
- tag immagini coerenti con il run della pipeline;
- file di evidenza compilato.

## Evidenze

Usa:

```text
docs/template_evidence_ud15.md
```

come base per il tuo report.
