# UD12 - Docker locale: singola applicazione containerizzata e osservabile

## Scopo della UD

Questa unità didattica serve a consolidare il concetto di **immagine container** e di **container locale** prima di introdurre, nei passaggi successivi del percorso, registry e deploy automatizzati.

In questa UD non usiamo ancora:

- Azure DevOps Pipeline operative;
- Azure Container Registry;
- Azure Container Instances;
- Azure Container Apps;
- Docker Compose;
- stack Prometheus/Grafana;
- Application Insights.

Il focus è volutamente più ristretto:

```text
codice sorgente
   -> Dockerfile
   -> docker build
   -> immagine Docker locale
   -> docker run
   -> container locale
   -> test HTTP
   -> log del container
```

## Sequenza consigliata di studio ed esecuzione

Eseguire i file in questo ordine:

1. `00_OBS_UD12_Concetti_Docker_Locale_App_Singola_v5_5.md`  
   Lettura concettuale: immagine, container, Dockerfile, porta, log, ciclo build/run/test.

2. `01_OBS_UD12_LAB_guidato_Docker_Locale_App_Singola_v5_5.md`  
   Laboratorio guidato: creazione app Flask, test senza Docker, Dockerfile, build immagine, run container, test endpoint e log.

3. `04_OBS_UD12_GUIDA_OPERATIVA_Docker_Comandi_Base_v5_5.md`  
   Guida di supporto da tenere aperta durante il laboratorio: comandi Docker essenziali e troubleshooting.

4. `02_OBS_UD12_MINI_ATTIVITA_Immagine_Container_Log_v5_5.md`  
   Mini-attività di consolidamento: ricostruzione del flusso codice -> immagine -> container -> log.

5. `03_OBS_UD12_LAB_autonomo_Containerizzazione_Verifica_Log_v5_5.md`  
   Laboratorio autonomo: nuova immagine, porta alternativa, verifiche HTTP, log ed evidenze.

6. `05_OBS_UD12_Raccordo_DevOps_Immagine_Container_v5_5.md`  
   Raccordo finale: perché l'immagine costruita localmente diventa l'unità tecnica che può essere usata da un flusso DevOps automatizzato.

## File sorgenti forniti

La cartella:

```text
src/app_base/
```

contiene una base già pronta con:

```text
src/app_base/
├── src/app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

Nel laboratorio guidato i partecipanti possono creare i file passo passo oppure confrontarsi con questa base.

## Evidenze da produrre

Durante la UD il partecipante deve produrre:

```text
docs/evidence_ud12.md
```

La traccia è indicata nel laboratorio guidato e nel laboratorio autonomo. È disponibile anche un template in:

```text
docs/template_evidence_ud12.md
```

## Risultato atteso finale

Alla fine della UD il partecipante deve saper dimostrare:

1. di avere verificato Docker locale;
2. di avere creato o esaminato una piccola applicazione osservabile;
3. di avere testato l'applicazione senza Docker;
4. di avere scritto un `Dockerfile`;
5. di avere costruito una immagine Docker;
6. di avere avviato un container;
7. di avere esposto correttamente una porta;
8. di avere verificato gli endpoint HTTP;
9. di avere letto i log del container;
10. di sapere distinguere codice, immagine e container.

## Nota metodologica

Questa UD non deve essere svolta come una raccolta di comandi da copiare. Ogni comando deve essere collegato a una domanda tecnica:

- che cosa sto costruendo?
- che cosa sto eseguendo?
- dove sta girando il processo?
- quale porta sto usando?
- dove vedo i log?
- cosa cambia se modifico il codice e ricostruisco l'immagine?
