# OBS_UD05 - Laboratorio guidato

# Azure Portal, IaaS, PaaS, SaaS e preparazione risorse per UD06

## 1. Obiettivo

In questo laboratorio usiamo Azure Portal per creare e documentare un piccolo ambiente di laboratorio.

L'ambiente dovrà restare disponibile per la UD06.

Obiettivi:

```text
verificare subscription e contesto Azure
creare o verificare Resource Group e tag
controllare Cost Management
creare un servizio PaaS statico con Storage Account
creare un App Service minimale
creare o analizzare una VM Linux controllata
analizzare un'offerta SaaS da Marketplace senza sottoscriverla
compilare un report IaaS/PaaS/SaaS
salvare inventario risorse per UD06
non eliminare le risorse a fine UD05
```

---

## 2. Avviso operativo prima della pratica

Ricordare che:

```text
Le risorse create oggi servono per la UD06.
Non dobbiamo eliminare il Resource Group durante la UD05.
Non dobbiamo fare cleanup completo a fine UD05.
La VM può essere fermata/deallocata solo se indicato dal docente.
Il cleanup definitivo verrà deciso dopo la UD06.
```


---

## 3. Preparazione locale

Questa preparazione va eseguita nel repository locale del partecipante, ad esempio in WSL.

Creare le cartelle:

```bash
mkdir -p docs evidence logs
```

Creare il report:

```bash
touch docs/report_ud05_azure_portal_iaas_paas_saas.md
```

Verificare di trovarsi nella cartella corretta del repository:

```bash
pwd
git status
```

---

## 4. Nota importante su WSL, terminale locale e Cloud Shell

Nel laboratorio produciamo file di evidenza dentro il repository locale, nelle cartelle:

```text
docs/
evidence/
logs/
```

Queste cartelle si trovano nell'ambiente locale del partecipante, ad esempio WSL.

Azure Cloud Shell è invece un ambiente remoto eseguito nel Portale Azure. Se in Cloud Shell eseguiamo un comando come:

```bash
az account show --output json > evidence/ud05_account_context.json
```

il file viene creato dentro Cloud Shell, non automaticamente nel repository locale.

Per questo motivo:

```text
i comandi che salvano file con > evidence/... devono essere eseguiti in WSL o nel terminale locale;
Cloud Shell può essere usata per verifiche rapide e output da copiare nel report;
gli screenshot devono essere salvati manualmente nella cartella evidence/ del repository locale;
prima del commit finale dobbiamo verificare da WSL che i file siano realmente presenti.
```

Verifica finale dei file locali:

```bash
find docs evidence -maxdepth 2 -type f | sort
git status
```

---

## 5. Codice partecipante

Usare un codice breve.

Esempio:

```text
mrossi
```

Regole:

```text
minuscolo
senza spazi
senza accenti
solo lettere, numeri e trattino dove consentito
```

Nel seguito useremo:

```text
<codice>
```

Sostituirlo con il proprio codice.

---

## 6. Naming della UD05

Nomi consigliati:

| Oggetto | Nome |
|---|---|
| Resource Group | `rg-obs-ud05-<codice>` |
| Storage Account | `stobsud05<codice>01`, senza trattini |
| App Service | `app-obs-ud05-<codice>` |
| VM | `vm-obs-ud05-<codice>` |
| Budget | `budget-obs-ud05-<codice>` |

Tag obbligatori:

| Tag | Valore |
|---|---|
| `corso` | `observability` |
| `ud` | `05` |
| `ambiente` | `lab` |
| `owner` | `<codice>` |
| `deleteAfter` | data indicata dal docente |
| `keepForUD06` | `true` |

Il tag `keepForUD06=true` serve a rendere esplicito che le risorse non devono essere eliminate alla fine della UD05.

---

## 7. Verifica contesto Azure

Dal Portale:

```text
https://portal.azure.com
```

Verificare:

```text
account
directory/tenant
subscription
```

### 7.1 Opzione A - Azure CLI in WSL o terminale locale

Usare questa opzione se Azure CLI è installata nel proprio ambiente locale e il comando `az account show` funziona.

Eseguire da WSL o terminale locale, dentro il repository:

```bash
mkdir -p evidence

az account show --output json > evidence/ud05_account_context.json

az account show   --query "{name:name,id:id,tenantId:tenantId,user:user.name}"   --output table
```

In questo caso il file:

```text
evidence/ud05_account_context.json
```

viene salvato direttamente nel repository locale e potrà essere aggiunto al commit finale.

### 7.2 Opzione B - Azure Cloud Shell

Usare questa opzione se si lavora dal Portale Azure con Cloud Shell.

Eseguire in Cloud Shell:

```bash
az account show   --query "{name:name,id:id,tenantId:tenantId,user:user.name}"   --output table
```

In Cloud Shell l'output viene prodotto nell'ambiente remoto di Azure, non nel repository locale del partecipante.

In questo caso:

```text
copiare i valori principali nel report;
salvare uno screenshot del contesto Azure;
non dare per scontato che un file creato in Cloud Shell finisca nella cartella evidence/ locale.
```

Evidenza richiesta:

```text
evidence/01_subscription_context.png
```

Nel report compilare:

```text
Subscription:
Tenant:
Utente:
Data/ora:
Modalità usata:
[ ] Azure CLI locale / WSL
[ ] Azure Cloud Shell
```

---

## 8. Resource Group e tag

Dal Portale:

```text
Resource groups -> Create
```

Creare:

```text
rg-obs-ud05-<codice>
```

Regione consigliata:

```text
West Europe
```

Se la regione non è disponibile, utilizzare un'area geograficamente vicina o quella indicata dal docente.

Applicare i tag obbligatori, incluso:

```text
keepForUD06=true
```

### 8.1 Verifica da Azure CLI locale / WSL

Eseguire da WSL o terminale locale, dentro il repository:

```bash
export RG_NAME="rg-obs-ud05-<codice>"

az group show   --name "$RG_NAME"   --output json > evidence/ud05_resource_group.json
```

Visualizzare i tag:

```bash
az group show   --name "$RG_NAME"   --query "tags"   --output table
```

### 8.2 Verifica da Cloud Shell

Eseguire in Cloud Shell solo la vista sintetica:

```bash
RG_NAME="rg-obs-ud05-<codice>"

az group show   --name "$RG_NAME"   --query "{name:name,location:location,tags:tags}"   --output table
```

Copiare i valori principali nel report.

Evidenza:

```text
evidence/02_resource_group_tags.png
```

---

## 9. Cost Management

Prima dei deploy aprire:

```text
Cost Management + Billing
```

Controllare:

```text
subscription corretta
costi correnti
forecast, se disponibile
budget, se disponibile
```

Se la subscription consente budget, creare:

```text
budget-obs-ud05-<codice>
```

Importo basso, secondo indicazione docente.

Se la subscription non consente budget, salvare screenshot dell'overview costi e annotare il motivo.

Evidenza:

```text
evidence/03_cost_management_budget_or_overview.png
```

---

## 10. PaaS 1 - Storage Account con static website

### 10.1 Obiettivo

Creiamo un servizio PaaS semplice: static website su Storage Account.

Non gestiamo server Web o sistema operativo. Gestiamo configurazione e contenuto statico.

### 10.2 Creazione file HTML

Creare localmente, nel repository:

```text
index.html
```

Contenuto:

```html
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>OBS UD05 - Static Website</title>
</head>
<body>
  <h1>OBS UD05 - Static Website</h1>
  <p>Pagina pubblicata tramite Azure Storage static website.</p>
  <p>Modello cloud: PaaS.</p>
  <p>Partecipante: <codice></p>
</body>
</html>
```

Sostituire `<codice>` con il proprio codice partecipante.

### 10.3 Creazione Storage Account

Dal Portale:

```text
Storage accounts -> Create
```

Impostazioni consigliate:

| Campo | Valore |
|---|---|
| Resource Group | `rg-obs-ud05-<codice>` |
| Storage account name | `stobsud05<codice>01` |
| Region | stessa del Resource Group |
| Performance | Standard |
| Redundancy | LRS |
| Access tier | Hot, se richiesto |
| Tags | tag obbligatori |

Il nome dello Storage Account deve essere globalmente univoco, minuscolo, senza trattini.

### 10.4 Abilitazione static website

Aprire lo Storage Account.

Andare in:

```text
Static website
```

Impostare:

```text
Enabled
Index document name: index.html
```

Salvare.

Azure crea il container:

```text
$web
```

Caricare `index.html` nel container `$web`.

Aprire l'endpoint static website e verificare la pagina.

### 10.5 Evidenze

Salvare:

```text
evidence/04_storage_static_website.png
```

### 10.6 Verifica da Azure CLI locale / WSL

Eseguire da WSL o terminale locale, dentro il repository:

```bash
export STORAGE_NAME="stobsud05<codice>01"

az storage account show   --name "$STORAGE_NAME"   --resource-group "$RG_NAME"   --output json > evidence/ud05_storage_account.json
```

### 10.7 Verifica da Cloud Shell

Eseguire in Cloud Shell solo la vista sintetica:

```bash
STORAGE_NAME="stobsud05<codice>01"
RG_NAME="rg-obs-ud05-<codice>"

az storage account show   --name "$STORAGE_NAME"   --resource-group "$RG_NAME"   --query "{name:name,location:location,kind:kind,sku:sku.name}"   --output table
```

Copiare i valori principali nel report.

Nel report indicare:

```text
Nome Storage Account:
Endpoint static website:
Perché è PaaS:
Rischi/costi residui:
```

---

## 11. PaaS 2 - App Service minimale

### 11.1 Obiettivo

Creiamo una Web App minima su App Service.

App Service è PaaS perché Azure gestisce infrastruttura e piattaforma di hosting. Noi scegliamo runtime, piano e configurazione base.

### 11.2 Creazione Web App

Dal Portale:

```text
App Services -> Create -> Web App
```

Impostazioni consigliate:

| Campo | Valore |
|---|---|
| Resource Group | `rg-obs-ud05-<codice>` |
| Name | `app-obs-ud05-<codice>` |
| Publish | Code |
| Runtime stack | Node LTS o Python, secondo disponibilità |
| Operating System | Linux, se disponibile |
| Region | stessa del Resource Group |
| App Service Plan | nuovo |
| Pricing plan | Free F1, se disponibile |
| Tags | tag obbligatori |

Se il piano gratuito non è disponibile, non scegliere piani costosi senza autorizzazione.

### 11.3 Verifica

Aprire la Web App.

Controllare:

```text
Overview
Default domain
Status
App Service Plan
```

Aprire l'URL nel browser.

Evidenza:

```text
evidence/05_app_service_overview.png
```

### 11.4 Verifica da Azure CLI locale / WSL

Eseguire da WSL o terminale locale, dentro il repository:

```bash
export APP_NAME="app-obs-ud05-<codice>"

az webapp show   --name "$APP_NAME"   --resource-group "$RG_NAME"   --output json > evidence/ud05_app_service.json
```

### 11.5 Verifica da Cloud Shell

Eseguire in Cloud Shell solo la vista sintetica:

```bash
APP_NAME="app-obs-ud05-<codice>"
RG_NAME="rg-obs-ud05-<codice>"

az webapp show   --name "$APP_NAME"   --resource-group "$RG_NAME"   --query "{name:name,state:state,defaultHostName:defaultHostName,kind:kind}"   --output table
```

Copiare i valori principali nel report.

Nel report indicare:

```text
Nome App Service:
URL:
Runtime:
Pricing plan:
Perché è PaaS:
```

---

## 12. IaaS - VM Linux controllata

## Avviso prima della VM

La VM è la risorsa più delicata per costo e quota.

Crearla solo se il docente autorizza.

Modalità possibili:

| Modalità | Uso |
|---|---|
| Demo docente | classe inesperta o subscription fragili |
| Coppie | meno risorse e meno costo |
| Individuale | solo se autorizzato |

### 12.1 Creazione VM

Dal Portale:

```text
Virtual machines -> Create -> Azure virtual machine
```

Impostazioni consigliate:

| Campo | Valore |
|---|---|
| Resource Group | `rg-obs-ud05-<codice>` |
| VM name | `vm-obs-ud05-<codice>` |
| Image | Ubuntu Server LTS |
| Size | B1s o SKU economica autorizzata |
| Authentication | secondo indicazione docente |
| Public inbound ports | None, se non serve accesso |
| OS disk | Standard SSD/HDD economico |
| Public IP | None se consentito |
| Tags | tag obbligatori |

Non aprire porte inutili.

Non trasformare questa sezione in laboratorio Linux: lo scopo è capire IaaS e lasciare una VM osservabile per UD06.

### 12.2 Verifica VM

Aprire Overview della VM.

Annotare:

```text
stato
size
Resource Group
disco
rete
IP pubblico, se presente
NSG
```

Evidenza:

```text
evidence/06_vm_overview_or_deallocated.png
```

### 12.3 Verifica da Azure CLI locale / WSL

Eseguire da WSL o terminale locale, dentro il repository:

```bash
export VM_NAME="vm-obs-ud05-<codice>"

az vm show   --name "$VM_NAME"   --resource-group "$RG_NAME"   --output json > evidence/ud05_vm.json
```
**Attenzione:**
per evitare errore di versione più recente del modulo AZ CLI, è possibile utilizzare il seguente comando:

```bash
az vm list -g "$RG_NAME" -o json > evidence/ud05_vm.json
```
Per ottenere una vista sintetica dello stato della VM:

```bash
az vm get-instance-view   --name "$VM_NAME"   --resource-group "$RG_NAME"   --query "instanceView.statuses[].displayStatus"   --output table
```

### 12.4 Verifica da Cloud Shell

Eseguire in Cloud Shell solo la vista sintetica:

```bash
VM_NAME="vm-obs-ud05-<codice>"
RG_NAME="rg-obs-ud05-<codice>"

az vm show   --name "$VM_NAME"   --resource-group "$RG_NAME"   --query "{name:name,location:location,vmSize:hardwareProfile.vmSize}"   --output table

az vm get-instance-view   --name "$VM_NAME"   --resource-group "$RG_NAME"   --query "instanceView.statuses[].displayStatus"   --output table
```

Copiare i valori principali nel report.

### 12.5 Controllo costo VM

Se il docente lo richiede, fermare/deallocare la VM dal Portale:

```text
VM -> Stop
```

Verificare che lo stato sia:

```text
Stopped (deallocated)
```

Importante:

```text
Fermare/deallocare non significa eliminare.
La VM e le risorse collegate devono restare disponibili per UD06.
```

Nel report indicare:

```text
VM creata o analizzata:
Modalità: demo / coppia / individuale
Stato finale:
Perché è IaaS:
Rischi/costi residui:
```

---

## 13. SaaS - Marketplace analysis senza acquisto

Aprire:

```text
Marketplace
```

Cercare una categoria, ad esempio:

```text
monitoring
backup
security
crm
project management
```

Scegliere un'offerta SaaS e analizzarla.

Non sottoscrivere.

Fermarsi prima di:

```text
Subscribe
Buy
Get it now
Create
Start trial
```

Evidenza:

```text
evidence/07_marketplace_saas_analysis.png
```

Nel report compilare:

| Campo | Risposta |
|---|---|
| Nome offerta |  |
| Publisher |  |
| Categoria |  |
| Pricing visibile |  |
| Trial |  |
| Perché è SaaS |  |
| Rischi lock-in/dati/costi |  |

---

## 14. Inventario finale per UD06

Questa sezione è obbligatoria.

### 14.1 Inventario da Azure CLI locale / WSL

Eseguire da WSL o terminale locale, dentro il repository:

```bash
az resource list   --resource-group "$RG_NAME"   --output json > evidence/08_rg_inventory_for_ud06.json
```

Vista sintetica:

```bash
az resource list   --resource-group "$RG_NAME"   --query "[].{name:name,type:type,location:location}"   --output table
```

Salvare anche Activity Log recente:

```bash
az monitor activity-log list   --resource-group "$RG_NAME"   --max-events 20   --output json > evidence/ud05_activity_log_for_ud06.json
```

### 14.2 Inventario da Cloud Shell

Eseguire in Cloud Shell le viste sintetiche:

```bash
RG_NAME="rg-obs-ud05-<codice>"

az resource list   --resource-group "$RG_NAME"   --query "[].{name:name,type:type,location:location}"   --output table

az monitor activity-log list   --resource-group "$RG_NAME"   --max-events 20   --query "[].{time:eventTimestamp,operation:operationName.value,status:status.value,resource:resourceGroupName}"   --output table
```

Copiare i risultati principali nel report.

Se il docente richiede anche i file JSON locali, copiare l'output da Cloud Shell e incollarlo manualmente in file locali dentro `evidence/`, oppure rieseguire i comandi da WSL con Azure CLI locale.

Nel report indicare:

```text
Risorse lasciate per UD06:
- Storage Account:
- App Service:
- VM:
- App Service Plan:
- Disk:
- Network Interface:
- Network Security Group:
- Virtual Network:
- Public IP, se presente:
```

---

## 15. Report finale

Compilare:

```text
docs/report_ud05_azure_portal_iaas_paas_saas.md
```

Template:

```markdown
# Report UD05 - Azure Portal, IaaS, PaaS, SaaS

## 1. Contesto

Partecipante:
Codice:
Data:
Subscription:
Tenant:
Regione:
Resource Group:
Modalità CLI usata:
[ ] Azure CLI locale / WSL
[ ] Azure Cloud Shell

## 2. Vincolo UD06

Ho compreso che le risorse devono restare disponibili per UD06:
[ ] Sì
[ ] No

## 3. Resource Group e tag

Nome:
Tag applicati:
Screenshot:

## 4. Cost Management

Budget creato:
[ ] Sì
[ ] No

Motivo se non creato:
Evidenza:

## 5. PaaS - Storage static website

Storage Account:
Endpoint:
Perché è PaaS:
Evidenze:

## 6. PaaS - App Service

Nome:
URL:
Runtime:
Pricing plan:
Perché è PaaS:
Evidenze:

## 7. IaaS - VM Linux

Modalità:
Nome VM:
Size:
Stato finale:
Public IP:
Perché è IaaS:
Rischi/costi residui:
Evidenze:

## 8. SaaS - Marketplace analysis

Offerta:
Publisher:
Categoria:
Pricing/trial:
Perché è SaaS:
Rischi:
Evidenze:

## 9. Tabella comparativa

| Aspetto | IaaS VM | PaaS Storage static website | PaaS App Service | SaaS Marketplace |
|---|---|---|---|---|
| Cosa configuriamo noi |  |  |  |  |
| Gestiamo OS |  |  |  |  |
| Gestiamo runtime |  |  |  |  |
| Gestiamo codice/contenuto |  |  |  |  |
| Dove può nascere costo |  |  |  |  |
| Segnali utili per UD06 |  |  |  |  |

## 10. Risorse lasciate per UD06

| Risorsa | Nome | Stato | Note costo |
|---|---|---|---|

## 11. Controllo finale no-cleanup

Ho verificato che il Resource Group esiste ancora:
[ ] Sì

Ho verificato che le risorse principali non sono state eliminate:
[ ] Sì

Ho salvato inventario per UD06:
[ ] Sì

## 12. Conclusione

Cosa ho imparato sui modelli IaaS/PaaS/SaaS:
Cosa dovremo osservare in UD06:
```

---

## 16. Chiusura della UD05 - non fare cleanup completo

Alla fine della UD05:

```text
NON eliminare il Resource Group.
NON eliminare Storage Account.
NON eliminare App Service.
NON eliminare VM, disco, rete o IP.
NON eliminare App Service Plan.
```

Consentito, se indicato dal docente:

```text
fermare/deallocare la VM
controllare Cost Management
salvare screenshot
salvare inventario
fare commit/push
```

Evidenza finale:

```text
evidence/09_no_cleanup_final_check.png
```

---

## 17. Commit e push

Verificare da WSL o terminale locale:

```bash
find docs evidence -maxdepth 2 -type f | sort
git status
```

Commit consigliato:

```bash
git add docs evidence index.html
git commit -m "Add UD05 Azure Portal IaaS PaaS SaaS report"
git push
```

---

## 18. Checklist finale

```text
[ ] contesto Azure verificato
[ ] modalità CLI indicata nel report
[ ] Resource Group creato/verificato
[ ] tag applicati, incluso keepForUD06=true
[ ] Cost Management controllato
[ ] Storage static website creato/verificato
[ ] App Service creato/verificato
[ ] VM creata/analizzata secondo indicazione docente
[ ] Marketplace SaaS analizzato senza sottoscrizione
[ ] report compilato
[ ] inventario per UD06 salvato o riportato nel report
[ ] risorse NON eliminate
[ ] eventuale VM fermata/deallocata, se richiesto
[ ] file locali verificati da WSL prima del commit
[ ] commit/push eseguito, se richiesto
```
