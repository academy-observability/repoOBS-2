# OBS UD16 - Deploy FE/BE su Azure Container Apps

## Scopo

In UD16 portiamo in cloud il sistema frontend/backend preparato in UD15.

La UD15 ha prodotto due immagini in Azure Container Registry:

```text
backend:<tag>
frontend:<tag>
```

La UD16 usa quelle immagini e crea due Azure Container Apps:

```text
ca-obs-ud16-backend
ca-obs-ud16-frontend
```

Il frontend riceve una variabile `BACKEND_URL` e usa quell'URL per chiamare il backend.

## Cosa si fa

1. Verifichiamo le immagini ACR prodotte in UD15.
2. Creiamo o verifichiamo un Azure Container Apps Environment.
3. Creiamo la Container App backend.
4. Recuperiamo il FQDN del backend.
5. Creiamo la Container App frontend configurando `BACKEND_URL`.
6. Testiamo il frontend e la comunicazione frontend -> backend.
7. Osserviamo revisioni e log.
8. Documentiamo le evidenze.

## Cosa non si fa in UD16

- Non ricostruiamo le immagini: quello è UD15.
- Non introduciamo ancora Application Insights/OpenTelemetry: quello è UD17.
- Non usiamo lo stack locale Prometheus/Grafana/Jaeger: quello parte da UD18.
- Non facciamo produzione enterprise: lavoriamo su un modello didattico leggibile.

## Sequenza consigliata

```text
00 Concetti
07 Guida architettura ACA FE/BE
04 Guida operativa
01 Lab guidato
02 Mini-attività
03 Lab autonomo
05 Raccordo finale
```

## File principali

```text
00_OBS_UD16_Concetti_Azure_Container_Apps_FE_BE_v5_6.md
01_OBS_UD16_LAB_guidato_Deploy_FE_BE_Azure_Container_Apps_v5_6.md
02_OBS_UD16_MINI_ATTIVITA_Mappa_ACR_ACA_FE_BE_v5_6.md
03_OBS_UD16_LAB_autonomo_Nuova_Revisione_FE_BE_ACA_v5_6.md
04_OBS_UD16_GUIDA_OPERATIVA_ACA_Revisioni_Log_BackendURL_v5_6.md
05_OBS_UD16_Raccordo_Deploy_FE_BE_Cloud_v5_6.md
07_OBS_UD16_GUIDA_ARCHITETTURA_FE_BE_ACA_RETE_INGRESS_REVISIONI_v5_6.md
templates/azure-pipelines-ud16-deploy-aca.yml
docs/template_evidence_ud16.md
```

## Output atteso

Al termine il partecipante deve poter dire:

> Ho preso le due immagini frontend/backend pubblicate in ACR in UD15 e le ho distribuite su Azure Container Apps. Il backend ha un FQDN, il frontend ha un FQDN e il frontend chiama il backend tramite `BACKEND_URL`. So leggere revisioni, log e stato delle Container Apps.
