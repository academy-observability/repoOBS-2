# UD13 - Primo deploy automatico cloud con GitHub, Azure DevOps, ACR e ACI

## Scopo della UD

Questa unità didattica porta nel cloud il lavoro fatto in Docker locale.

Nella UD precedente il partecipante ha costruito ed eseguito una immagine sul proprio PC. In questa UD il partecipante automatizza il flusso:

```text
codice su GitHub
   -> pipeline Azure DevOps
   -> docker build su agent
   -> push immagine su Azure Container Registry
   -> deploy su Azure Container Instances
   -> test HTTP via FQDN
   -> log cloud del container
```

## Cosa non si fa in questa UD

In questa UD non si affrontano ancora:

- applicazione frontend/backend;
- Azure Container Apps;
- Application Insights;
- Docker Compose;
- Prometheus/Grafana;
- rollback strutturato;
- gestione enterprise dei segreti.

ACI viene usato come primo target cloud semplice per capire il ciclo automatico.

## Sequenza consigliata di studio ed esecuzione

Eseguire i file in questo ordine:

1. `00_OBS_UD13_Concetti_Primo_Deploy_Automatico_ACR_ACI_v5_5.md`  
   Lettura concettuale: differenza tra Docker locale, pipeline, ACR e ACI.

2. `04_OBS_UD13_GUIDA_OPERATIVA_Service_Connections_ACR_ACI_v5_5.md`  
   Guida di supporto da tenere aperta durante il laboratorio: service connection, ACR, ACI, troubleshooting.

3. `01_OBS_UD13_LAB_guidato_GitHub_AzureDevOps_ACR_ACI_v5_5.md`  
   Laboratorio guidato: creazione app, pipeline, build, push su ACR e deploy su ACI.

4. `02_OBS_UD13_MINI_ATTIVITA_Mappa_Pipeline_ACR_ACI_v5_5.md`  
   Mini-attività di consolidamento sul flusso GitHub -> Azure DevOps -> ACR -> ACI.

5. `03_OBS_UD13_LAB_autonomo_Rilascio_Nuova_Versione_ACI_v5_5.md`  
   Laboratorio autonomo: modifica versione, nuovo commit, nuova immagine, nuovo deploy e verifica.

6. `05_OBS_UD13_Raccordo_Docker_Locale_Deploy_Automatico_v5_5.md`  
   Raccordo finale: passaggio concettuale da container locale a deploy automatico cloud.

## File sorgenti forniti

La cartella:

```text
src/app_base/
```

contiene una base applicativa già pronta con:

```text
src/app_base/
├── src/app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

La cartella:

```text
templates/
```

contiene un template di pipeline:

```text
templates/azure-pipelines-ud13.yml
```

## Evidenze da produrre

Durante la UD il partecipante deve produrre:

```text
docs/evidence_ud13.md
```

È disponibile un template in:

```text
docs/template_evidence_ud13.md
```

## Risultato atteso finale

Alla fine della UD il partecipante deve saper dimostrare:

1. di avere una app containerizzabile;
2. di avere un file `azure-pipelines.yml` nel repository GitHub;
3. di avere creato o verificato ACR;
4. di avere configurato Azure DevOps per leggere GitHub e usare Azure;
5. di avere eseguito una pipeline Azure DevOps;
6. di avere pubblicato una immagine su ACR;
7. di avere creato un container ACI dalla pipeline;
8. di avere testato gli endpoint via FQDN;
9. di avere letto i log cloud con `az container logs`;
10. di sapere spiegare la differenza tra build, push e deploy.

## Nota sui costi e cleanup

A fine laboratorio il container ACI può essere eliminato. ACR può essere mantenuto se indicato dal docente, perché può servire nei passaggi successivi del percorso.
