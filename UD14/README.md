# UD14 - Pipeline multistage con ACR, ACI e smoke test

---

# Scopo della UD14

Questa unità migliora il primo deploy automatico già realizzato con GitHub, Azure DevOps, ACR e ACI.

L'obiettivo non è introdurre nuovi servizi cloud, ma migliorare la qualità della pipeline:

```text
ValidateRepository -> BuildAndPush -> DeployToACI -> SmokeTest
```

---

# Cosa faremo

Durante la UD14:

- prepareremo una cartella `work/UD14`;
- useremo una piccola app Flask containerizzata;
- creeremo una pipeline Azure DevOps multistage;
- costruiremo una immagine Docker tramite pipeline;
- pubblicheremo l'immagine in Azure Container Registry;
- distribuiremo il container su Azure Container Instances;
- eseguiremo smoke test automatici;
- verificheremo endpoint e log;
- produrremo evidenze tecniche.

---

# Cosa non faremo

In questa UD non faremo:

- applicazione frontend/backend;
- Azure Container Apps;
- Application Insights;
- Docker Compose;
- Prometheus/Grafana;
- rollback strutturato;
- approvazioni manuali di rilascio;
- gestione avanzata dei segreti.

---

# Sequenza consigliata dei file

Segui questo ordine:

```text
1. 00_OBS_UD14_Concetti_Pipeline_Multistage_SmokeTest_v5_5.md
2. 04_OBS_UD14_GUIDA_OPERATIVA_Debug_Pipeline_ACR_ACI_v5_5.md
3. 01_OBS_UD14_LAB_guidato_Pipeline_Multistage_ACR_ACI_v5_5.md
4. 02_OBS_UD14_MINI_ATTIVITA_Stage_Build_Deploy_SmokeTest_v5_5.md
5. 03_OBS_UD14_LAB_autonomo_Rilascio_Tracciabile_Multistage_v5_5.md
6. 05_OBS_UD14_Raccordo_Pipeline_Qualita_Rilascio_v5_5.md
```

La guida operativa viene letta prima del laboratorio perché contiene i controlli e il troubleshooting più frequenti.

---

# Struttura del pacchetto

```text
UD14/
├── 00_OBS_UD14_Concetti_Pipeline_Multistage_SmokeTest_v5_5.md
├── 01_OBS_UD14_LAB_guidato_Pipeline_Multistage_ACR_ACI_v5_5.md
├── 02_OBS_UD14_MINI_ATTIVITA_Stage_Build_Deploy_SmokeTest_v5_5.md
├── 03_OBS_UD14_LAB_autonomo_Rilascio_Tracciabile_Multistage_v5_5.md
├── 04_OBS_UD14_GUIDA_OPERATIVA_Debug_Pipeline_ACR_ACI_v5_5.md
├── 05_OBS_UD14_Raccordo_Pipeline_Qualita_Rilascio_v5_5.md
├── README.md
├── src/
│   └── app_base/
└── templates/
    └── azure-pipelines-ud14-multistage.yml
```

---

# Output atteso

Al termine della UD14 dovrai poter mostrare:

- pipeline Azure DevOps multistage funzionante;
- stage separati e leggibili;
- immagine pubblicata in ACR;
- container ACI creato;
- FQDN pubblico dell'applicazione;
- smoke test automatico riuscito;
- test manuali sugli endpoint;
- log cloud letti con `az container logs`;
- file `docs/evidence_ud14.md` compilato.

---

# Evidenze da produrre

Nel repository crea:

```text
work/UD14/docs/evidence_ud14.md
```

Il file deve documentare:

- obiettivo della pipeline multistage;
- Resource Group, ACR, ACI e service connection usati;
- struttura degli stage;
- Build ID e tag immagine;
- verifica ACR;
- verifica ACI;
- smoke test;
- test manuali;
- log cloud;
- eventuali problemi incontrati.

---

# Cleanup

A fine laboratorio puoi eliminare ACI:

```bash
az container delete \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --yes
```

Non eliminare ACR se il docente non lo richiede.
