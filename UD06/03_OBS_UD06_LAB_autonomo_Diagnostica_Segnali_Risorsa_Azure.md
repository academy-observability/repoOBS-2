# OBS_UD06 - Laboratorio autonomo

# Diagnostica dei segnali di una risorsa Azure

## 1. Obiettivo

Nel laboratorio autonomo analizziamo una risorsa Azure esistente e produciamo un report diagnostico.

Non dobbiamo creare nuove risorse.

Dobbiamo dimostrare di saper:

```text
identificare la risorsa
recuperare il Resource ID
leggere stato e proprietà
analizzare Activity Log
verificare metriche disponibili
leggere almeno una metrica recente
verificare Diagnostic Settings e categorie diagnostiche
collegare ogni segnale a una domanda diagnostica
```

## 2. Scenario assegnato

Autoassegnarsi uno o più scenari.

Indicare nel report:

```text
Scenario:
Risorsa:
Resource Group:
Subscription:
```

Scenari possibili:

| Scenario | Risorsa | Obiettivo |
|---|---|---|
| A | Storage Account | verificare traffico, metriche e categorie diagnostiche |
| B | App Service | verificare stato Web App, metriche richieste e log disponibili |
| C | VM Linux | verificare power state, metriche compute/rete/disco e costi potenziali |
| D | Resource Group | ricostruire eventi amministrativi recenti dal punto di vista Activity Log |

## 3. Metodo obbligatorio

Per ogni segnale usare questo schema:

```text
Domanda diagnostica:
Segnale scelto:
Comando o pagina usata:
Evidenza salvata:
Interpretazione:
```

Esempio:

```text
Domanda diagnostica:
La VM sta consumando compute?

Segnale scelto:
PowerState.

Comando:
az vm get-instance-view ...

Evidenza:
evidence/ud06_autonomo_vm_instance_view.json

Interpretazione:
La VM risulta deallocated, quindi non consuma compute VM, ma possono restare costi collegati a disco o IP.
```


## 4. Nota operativa su WSL, terminale locale e Cloud Shell

Nel laboratorio autonomo tutti i comandi che salvano file in `evidence/` devono essere eseguiti dal repository locale, normalmente in WSL o in un terminale locale con Azure CLI autenticata.

Azure Cloud Shell può essere usata per viste tabellari e controlli rapidi, ma non produce automaticamente file nel repository locale.

Regola pratica:

```text
Comando con > evidence/...  -> WSL o terminale locale nel repository.
Cloud Shell                 -> output da copiare nel report o screenshot.
```

## 5. Preparazione

Creare cartelle:

```bash
mkdir -p docs evidence
```

Creare report:

```bash
touch docs/report_ud06_autonomo_diagnostica_risorsa.md
```

Verificare contesto:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az account show --output json > evidence/ud06_autonomo_account_context.json
```

## 6. Identificazione risorsa

Impostare il Resource Group:

```bash
export RG_NAME="rg-obs-ud05-mrossi"
```

Elencare risorse:

```bash
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{name:name,type:type,location:location,id:id}" \
  --output table
```

Salvare inventario:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az resource list \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_autonomo_rg_inventory.json
```

Scegliere la risorsa assegnata e salvare il suo Resource ID nel report.

## 7. Activity Log

Salvare eventi recenti:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 20 \
  --output json > evidence/ud06_autonomo_activity_log.json
```

Nel report rispondere:

```text
Quali operazioni recenti sono visibili?
Ci sono operazioni fallite?
Gli eventi sono coerenti con quanto fatto in UD05?
```

## 8. Analisi della risorsa assegnata

Usare il comando corretto in base allo scenario.

### Scenario A - Storage Account

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
export STORAGE_NAME="<nome-storage>"

az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_autonomo_storage_details.json

export RESOURCE_ID="$(az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

### Scenario B - App Service

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
export APP_NAME="<nome-app-service>"

az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_autonomo_appservice_details.json

export RESOURCE_ID="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

### Scenario C - VM Linux

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
export VM_NAME="<nome-vm>"

az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_autonomo_vm_details.json

az vm get-instance-view \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_autonomo_vm_instance_view.json

export RESOURCE_ID="$(az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

### Scenario D - Resource Group

```bash
export RESOURCE_ID="$(az group show \
  --name "$RG_NAME" \
  --query id \
  --output tsv)"
```

## 9. Metriche

Se la risorsa supporta metriche:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az monitor metrics list-definitions \
  --resource "$RESOURCE_ID" \
  --output json > evidence/ud06_autonomo_metric_definitions.json
```

Vista sintetica:

```bash
az monitor metrics list-definitions \
  --resource "$RESOURCE_ID" \
  --query "[].{name:name.value,unit:unit,aggregation:primaryAggregationType}" \
  --output table
```

Scegliere una metrica sensata.

Esempi:

| Risorsa | Metrica candidata |
|---|---|
| Storage Account | `Transactions` |
| App Service | `Requests` |
| VM | `Percentage CPU` |

Eseguire:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az monitor metrics list \
  --resource "$RESOURCE_ID" \
  --metric "<NOME_METRICA>" \
  --interval PT5M \
  --output json > evidence/ud06_autonomo_metric_values.json
```

Nel report indicare:

```text
metrica scelta
time range implicito/default o impostato
intervallo
aggregazione osservata
presenza o assenza di valori
interpretazione
```

## 10. Diagnostic Settings

Verificare categorie:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az monitor diagnostic-settings categories list \
  --resource "$RESOURCE_ID" \
  --output json > evidence/ud06_autonomo_diagnostic_categories.json
```

Verificare settings esistenti:

```bash
# Eseguire da WSL o terminale locale dentro il repository: l'output viene salvato in evidence/.
az monitor diagnostic-settings list \
  --resource "$RESOURCE_ID" \
  --output json > evidence/ud06_autonomo_diagnostic_settings.json
```

Nel report rispondere:

```text
La risorsa espone categorie diagnostiche?
Esiste già un Diagnostic Setting?
Se non esiste, quale dato non stiamo raccogliendo?
Verso quale destinazione avrebbe senso inviare i log nelle UD successive?
```

## 11. Report autonomo

Compilare:

```text
docs/report_ud06_autonomo_diagnostica_risorsa.md
```

Template:

```markdown
# Report autonomo UD06 - Diagnostica segnali risorsa Azure

## 1. Scenario

Scenario assegnato:
Risorsa:
Resource Group:
Subscription:
Data/ora:

## 2. Identificazione risorsa

Nome:
Tipo:
Resource ID:
Regione:
Tag rilevanti:

## 3. Domande diagnostiche

| Domanda | Segnale | Evidenza |
|---|---|---|
|  |  |  |

## 4. Activity Log

Eventi osservati:
Failure:
Interpretazione:

## 5. Stato e proprietà

Stato rilevato:
Proprietà rilevanti:
Interpretazione:

## 6. Metriche

Metriche disponibili:
Metrica scelta:
Valori recenti:
Time range/intervallo:
Interpretazione:

## 7. Diagnostic Settings

Categorie disponibili:
Settings esistenti:
Destinazione:
Interpretazione:

## 8. Conclusione diagnostica

Cosa posso affermare:
Cosa non posso affermare:
Quale configurazione sarebbe utile nella UD07:

## 9. Evidenze

- evidence/ud06_autonomo_account_context.json
- evidence/ud06_autonomo_rg_inventory.json
- evidence/ud06_autonomo_activity_log.json
- evidence/...
```

## 12. Checklist finale

```text
[ ] risorsa identificata con Resource ID
[ ] Activity Log salvato e interpretato
[ ] stato/proprietà salvati
[ ] metric definitions salvate
[ ] almeno una metrica letta o assenza dati motivata
[ ] Diagnostic Settings verificati
[ ] categorie diagnostiche verificate
[ ] report completato
[ ] evidenze salvate
[ ] commit/push eseguito, se richiesto
```

## 13. Commit

```bash
git status
git add docs evidence
git commit -m "Add UD06 autonomous Azure diagnostic signals report"
git push
```

