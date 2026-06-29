# OBS_UD05 - Laboratorio guidato

# Azure Portal, IaaS, PaaS, SaaS e preparazione risorse per UD06

## 1. Obiettivo

In questo laboratorio usiamo Azure Portal per creare e documentare un piccolo ambiente di laboratorio.

L'ambiente dovra restare disponibile per la UD06.

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

## 2. Avviso operativo prima della pratica

Prima di creare risorse leggere e confermare:

```text
Le risorse create oggi servono per la UD06.
Non dobbiamo eliminare il Resource Group durante la UD05.
Non dobbiamo fare cleanup completo a fine UD05.
La VM puo essere fermata/deallocata solo se indicato dal docente.
Il cleanup definitivo verra deciso dopo la UD06.
```



## 3. Preparazione locale

Creare cartelle:

```bash
mkdir -p docs evidence logs
```

Creare report:

```bash
touch docs/report_ud05_azure_portal_iaas_paas_saas.md
```

## 4. Codice partecipante

Usare un codice breve:

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

## 5. Naming della UD05

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

## 6. Verifica contesto Azure

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

Da Cloud Shell o Azure CLI:

```bash
az account show --output json > evidence/ud05_account_context.json
```

Vista sintetica:

```bash
az account show --query "{name:name,id:id,tenantId:tenantId,user:user.name}" --output table
```

Nel report compilare:

```text
Subscription:
Tenant:
Utente:
Data/ora:
```

Evidenza screenshot:

```text
evidence/01_subscription_context.png
```

## 7. Resource Group e tag

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

Se la regione non è disponibile, utilizzare altre zone geograficamente più vicine.

Applicare i tag obbligatori, incluso:

```text
keepForUD06=true
```

Verifica da CLI:

```bash
export RG_NAME="rg-obs-ud05-<codice>"

az group show \
  --name "$RG_NAME" \
  --output json > evidence/ud05_resource_group.json
```

Visualizzare tag:

```bash
az group show \
  --name "$RG_NAME" \
  --query "tags" \
  --output table
```

Evidenza:

```text
evidence/02_resource_group_tags.png
```

## 8. Cost Management

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

## 9. PaaS 1 - Storage Account con static website

### 9.1 Obiettivo

Creiamo un servizio PaaS semplice: static website su Storage Account.

Non gestiamo server Web o sistema operativo. Gestiamo configurazione e contenuto statico.

### 9.2 Creazione file HTML

Creare localmente:

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

### 9.3 Creazione Storage Account

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

### 9.4 Abilitazione static website

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

### 9.5 Evidenze

Salvare:

```text
evidence/04_storage_static_website.png
```

Da CLI, se disponibile:

```bash
export STORAGE_NAME="stobsud05<codice>01"

az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud05_storage_account.json
```

Nel report indicare:

```text
Nome Storage Account:
Endpoint static website:
Perche e PaaS:
Rischi/costi residui:
```

## 10. PaaS 2 - App Service minimale

### 10.1 Obiettivo

Creiamo una Web App minima su App Service.

App Service e PaaS perche Azure gestisce infrastruttura e piattaforma di hosting. Noi scegliamo runtime, piano e configurazione base.

### 10.2 Creazione Web App

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
| Runtime stack | Node LTS o Python, secondo disponibilita |
| Operating System | Linux, se disponibile |
| Region | stessa del Resource Group |
| App Service Plan | nuovo |
| Pricing plan | Free F1, se disponibile |
| Tags | tag obbligatori |

Se il piano gratuito non e disponibile, non scegliere piani costosi senza autorizzazione.

### 10.3 Verifica

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

Da CLI:

```bash
export APP_NAME="app-obs-ud05-<codice>"

az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud05_app_service.json
```

Nel report indicare:

```text
Nome App Service:
URL:
Runtime:
Pricing plan:
Perche e PaaS:
```

## 11. IaaS - VM Linux controllata

## Avviso prima della VM

La VM e la risorsa piu delicata per costo e quota.

Crearla solo se il docente autorizza.

Modalita possibili:

| Modalita | Uso |
|---|---|
| Demo docente | classe inesperta o subscription fragili |
| Coppie | meno risorse e meno costo |
| Individuale | solo se autorizzato |

### 11.1 Creazione VM

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

Non trasformare questa sezione in laboratorio Linux: lo scopo e capire IaaS e lasciare una VM osservabile per UD06.

### 11.2 Verifica VM

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

Da CLI:

```bash
export VM_NAME="vm-obs-ud05-<codice>"

az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud05_vm.json
```

### 11.3 Controllo costo VM

Se il docente lo richiede, fermare/deallocare la VM:

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
Modalita: demo / coppia / individuale
Stato finale:
Perche e IaaS:
Rischi/costi residui:
```

## 12. SaaS - Marketplace analysis senza acquisto

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
| Perche e SaaS |  |
| Rischi lock-in/dati/costi |  |

## 13. Inventario finale per UD06

Questa sezione e obbligatoria.

Creare inventario:

```bash
az resource list \
  --resource-group "$RG_NAME" \
  --output json > evidence/08_rg_inventory_for_ud06.json
```

Vista sintetica:

```bash
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{name:name,type:type,location:location}" \
  --output table
```

Salvare anche Activity Log recente:

```bash
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 20 \
  --output json > evidence/ud05_activity_log_for_ud06.json
```

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

## 14. Report finale

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

## 2. Vincolo UD06

Ho compreso che le risorse devono restare disponibili per UD06:
[ ] Si
[ ] No

## 3. Resource Group e tag

Nome:
Tag applicati:
Screenshot:

## 4. Cost Management

Budget creato:
[ ] Si
[ ] No

Motivo se non creato:
Evidenza:

## 5. PaaS - Storage static website

Storage Account:
Endpoint:
Perche e PaaS:
Evidenze:

## 6. PaaS - App Service

Nome:
URL:
Runtime:
Pricing plan:
Perche e PaaS:
Evidenze:

## 7. IaaS - VM Linux

Modalita:
Nome VM:
Size:
Stato finale:
Public IP:
Perche e IaaS:
Rischi/costi residui:
Evidenze:

## 8. SaaS - Marketplace analysis

Offerta:
Publisher:
Categoria:
Pricing/trial:
Perche e SaaS:
Rischi:
Evidenze:

## 9. Tabella comparativa

| Aspetto | IaaS VM | PaaS Storage static website | PaaS App Service | SaaS Marketplace |
|---|---|---|---|---|
| Cosa configuriamo noi |  |  |  |  |
| Gestiamo OS |  |  |  |  |
| Gestiamo runtime |  |  |  |  |
| Gestiamo codice/contenuto |  |  |  |  |
| Dove puo nascere costo |  |  |  |  |
| Segnali utili per UD06 |  |  |  |  |

## 10. Risorse lasciate per UD06

| Risorsa | Nome | Stato | Note costo |
|---|---|---|---|

## 11. Controllo finale no-cleanup

Ho verificato che il Resource Group esiste ancora:
[ ] Si

Ho verificato che le risorse principali non sono state eliminate:
[ ] Si

Ho salvato inventario per UD06:
[ ] Si

## 12. Conclusione

Cosa ho imparato sui modelli IaaS/PaaS/SaaS:
Cosa dovremo osservare in UD06:
```

## 15. Chiusura della UD05 - non fare cleanup completo

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

## 16. Commit e push

Verificare:

```bash
find docs evidence -maxdepth 2 -type f | sort
git status
```

Commit consigliato:

```bash
git add docs evidence
git commit -m "Add UD05 Azure Portal IaaS PaaS SaaS report"
git push
```

## 17. Checklist finale

```text
[ ] contesto Azure verificato
[ ] Resource Group creato/verificato
[ ] tag applicati, incluso keepForUD06=true
[ ] Cost Management controllato
[ ] Storage static website creato/verificato
[ ] App Service creato/verificato
[ ] VM creata/analizzata secondo indicazione docente
[ ] Marketplace SaaS analizzato senza sottoscrizione
[ ] report compilato
[ ] inventario per UD06 salvato
[ ] risorse NON eliminate
[ ] eventuale VM fermata/deallocata, se richiesto
[ ] commit/push eseguito, se richiesto
```

