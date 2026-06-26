# OBS UD05 - Laboratorio pratico: Azure Portal, IaaS, PaaS e SaaS

## 1. Scopo del laboratorio

Questo laboratorio deve essere svolto dopo il completamento del prerequisito di registrazione Azure.

L’obiettivo è prendere confidenza con il Portale Azure attraverso attività pratiche e controllate. Useremo l’interfaccia Web per creare, osservare e documentare risorse semplici, distinguendo i principali modelli di servizio cloud:

- IaaS, Infrastructure as a Service;
- PaaS, Platform as a Service;
- SaaS, Software as a Service.

La finalità non è imparare a monitorare Azure in profondità. Questo verrà trattato nelle UD successive. In questa UD lavoriamo soprattutto su orientamento nel Portale, creazione guidata di risorse, scelta di regione/SKU, Resource Group, tag, costi, modelli cloud e cleanup.

---

## 2. Cosa NON facciamo in questa UD

Per mantenere la progressione del corso, in questa UD non configuriamo:

- Azure Monitor in modo approfondito;
- Log Analytics Workspace;
- KQL;
- alert;
- workbook;
- dashboard;
- Application Insights;
- Diagnostic Settings;
- troubleshooting avanzato delle metriche;
- automazioni Infrastructure as Code;
- pipeline CI/CD;
- Kubernetes;
- container cloud.

Possiamo guardare la pagina **Overview** di una risorsa e, se utile, il suo **Activity Log** amministrativo. Non trasformiamo però questa UD in una lezione di monitoring, perché poi le UD successive esisterebbero solo per decorare il calendario, una pratica umana molto rispettata ma didatticamente discutibile.

---

## 3. Prerequisiti

Prima di iniziare dobbiamo avere:

```text
[ ] accesso a https://portal.azure.com
[ ] almeno una subscription Azure visibile
[ ] subscription in stato Enabled/attiva
[ ] Cloud Shell Bash funzionante
[ ] comando az account show già verificato nel prerequisito
[ ] consapevolezza di dove si trova Cost Management + Billing
[ ] spending limit non rimosso
```

In questo laboratorio useremo quasi sempre l’interfaccia Web. La CLI può essere utile solo per verifiche rapide, ma non è l’obiettivo principale.

---

## 4. Regole economiche e di sicurezza

Durante questo laboratorio creiamo risorse reali in Azure. Anche quando i costi sono bassi o nulli, una risorsa cloud resta una risorsa di fatturazione.

Regole obbligatorie:

1. creare solo le risorse richieste;
2. usare sempre il Resource Group indicato;
3. usare sempre i tag indicati;
4. scegliere SKU gratuite o economiche dove previsto;
5. non rimuovere lo spending limit;
6. non attivare servizi Marketplace a pagamento;
7. non creare VM non autorizzate dal docente;
8. non lasciare VM, dischi, IP pubblici o App Service Plan attivi se il docente richiede cleanup;
9. a fine laboratorio verificare Cost Management;
10. in caso di dubbio, fermarsi prima di premere **Create**, **Subscribe**, **Buy**, **Get it now** o equivalenti.

---

## 5. Durata prevista

Il laboratorio è pensato per una giornata da 8 ore.

| Fase | Durata indicativa | Attività |
|---|---:|---|
| 1 | 45 min | Orientamento nel Portale Azure |
| 2 | 45 min | Resource Group, naming, regioni, tag |
| 3 | 30 min | Cost Management e budget minimo |
| 4 | 90 min | PaaS 1: static website su Storage Account |
| 5 | 75 min | PaaS 2: App Service minimale |
| 6 | 75 min | IaaS: VM Linux minimale, demo/coppie/individuale |
| 7 | 45 min | SaaS: analisi Marketplace senza acquisto |
| 8 | 45 min | Report, confronto IaaS/PaaS/SaaS, cleanup finale |

La durata effettiva dipende dal numero di partecipanti, dallo stato delle subscription e dalla capacità del Portale di non comportarsi come un labirinto progettato da un comitato.

---

## 6. Nomi e tag da usare

### 6.1 Codice partecipante

Nel laboratorio useremo un codice personale breve.

Esempio:

```text
mrossi
```

Usare solo:

- lettere minuscole;
- numeri;
- eventualmente trattino `-` quando consentito;
- niente spazi;
- niente caratteri accentati.

Nel resto del documento useremo:

```text
<codice>
```

Sostituirlo con il proprio codice personale.

---

### 6.2 Resource Group

Nome consigliato:

```text
rg-obs-ud05-<codice>
```

Esempio:

```text
rg-obs-ud05-mrossi
```

Regione consigliata:

```text
West Europe
```

Se la regione non è disponibile, usare quella indicata dal docente.

---

### 6.3 Tag obbligatori

Applicare questi tag al Resource Group e, quando possibile, alle risorse create:

| Nome tag | Valore |
|---|---|
| `corso` | `observability` |
| `ud` | `05` |
| `ambiente` | `lab` |
| `owner` | `<codice>` |
| `deleteAfter` | data indicata dal docente, ad esempio `2026-06-30` |

I tag servono a riconoscere ownership, scopo, ambiente e data di eliminazione prevista. Non sono decorazioni: sono metadati di governance. Azure non è un armadio in cui buttare cose e sperare che nessuno apra l’anta.

---

## 7. File ed evidenze da produrre

Durante il laboratorio creeremo una cartella locale o nel repository della UD05 con questa struttura:

```text
docs/
  report_ud05_portal_iaas_paas_saas.md

evidence/
  01_portal_home_o_subscription.png
  02_resource_group_tags.png
  03_cost_management_budget_o_overview.png
  04_storage_static_website_overview.png
  05_static_website_endpoint.png
  06_app_service_overview.png
  07_app_service_default_page.png
  08_vm_overview_o_demo.png
  09_marketplace_saas_analysis.png
  10_cleanup_finale.png
```

Gli screenshot non devono includere dati personali sensibili, dati di pagamento o numeri completi di carta. Se compare un ID di subscription, tenant o billing account, oscurarlo se il report viene condiviso.

---

# Parte A - Orientamento nel Portale Azure

## 8. Accesso al Portale

Apriamo:

```text
https://portal.azure.com
```

Verifichiamo in alto a destra:

- account usato;
- directory/tenant corrente;
- eventuale possibilità di cambiare directory;
- lingua/interfaccia;
- notifiche.

### Evidenza

Salvare uno screenshot della Home o della pagina Subscriptions:

```text
evidence/01_portal_home_o_subscription.png
```

---

## 9. Ricerca delle risorse nel Portale

Nel Portale Azure quasi tutto parte dalla barra di ricerca in alto.

Cercare e aprire, senza modificare nulla:

```text
Subscriptions
Resource groups
Cost Management + Billing
Storage accounts
App Services
Virtual machines
Marketplace
```

Annotare nel report quali di questi servizi sono stati trovati facilmente e quali no.

### Domande guida

| Domanda | Risposta attesa |
|---|---|
| Dove vediamo la subscription corrente? | In Subscriptions o nel profilo/contesto del Portale |
| Dove creiamo un contenitore logico di risorse? | Resource groups |
| Dove controlliamo costi e budget? | Cost Management + Billing |
| Dove cerchiamo servizi SaaS? | Marketplace |

---

# Parte B - Resource Group, tag e costo minimo

## 10. Creazione del Resource Group

Dal Portale:

1. cercare `Resource groups`;
2. selezionare **Create**;
3. scegliere la subscription corretta;
4. impostare il nome:

```text
rg-obs-ud05-<codice>
```

5. selezionare la regione indicata dal docente, ad esempio:

```text
West Europe
```

6. aprire la sezione **Tags**;
7. inserire i tag obbligatori;
8. selezionare **Review + create**;
9. selezionare **Create**.

---

## 11. Verifica del Resource Group

Aprire il Resource Group appena creato.

Controllare:

- nome;
- regione;
- subscription;
- tag;
- sezione Overview;
- sezione Activity Log.

Non analizziamo in profondità l’Activity Log. In questa UD ci basta capire che Azure registra le operazioni amministrative, ad esempio creazione, modifica ed eliminazione di risorse.

### Evidenza

Salvare:

```text
evidence/02_resource_group_tags.png
```

---

## 12. Cost Management e budget minimo

Dal Portale:

1. cercare `Cost Management + Billing`;
2. entrare nel contesto della propria subscription;
3. cercare la sezione **Budgets**;
4. se disponibile, creare un budget minimo di laboratorio;
5. se la creazione del budget non è disponibile nella propria subscription, salvare comunque uno screenshot della pagina di riepilogo costi.

Valori consigliati, se il budget è disponibile:

| Campo | Valore consigliato |
|---|---|
| Nome | `budget-obs-ud05-<codice>` |
| Periodo | mensile |
| Importo | basso, ad esempio 5 o 10 nella valuta della subscription |
| Scope | subscription corrente |
| Alert | propria email, se richiesto e consentito |

Non tutte le subscription mostrano le stesse opzioni di billing. Se la voce Budget non è disponibile, annotarlo nel report.

### Evidenza

Salvare:

```text
evidence/03_cost_management_budget_o_overview.png
```

---

# Parte C - PaaS 1: static website su Storage Account

## 13. Obiettivo

Creiamo un piccolo sito statico usando Azure Storage.

Questo è un esempio di servizio PaaS perché non amministriamo un server Web, un sistema operativo o una macchina virtuale. Azure fornisce il servizio gestito di storage e hosting statico. Noi configuriamo la risorsa e carichiamo contenuto statico.

Il sito conterrà una pagina HTML minimale.

---

## 14. Creazione del file `index.html`

Sul proprio computer creare un file chiamato:

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
  <p>Questa pagina è pubblicata tramite Azure Storage static website.</p>
  <p>Modello cloud: PaaS.</p>
  <p>Partecipante: <codice></p>
</body>
</html>
```

Sostituire `<codice>` con il proprio codice personale.

---

## 15. Creazione dello Storage Account

Dal Portale:

1. cercare `Storage accounts`;
2. selezionare **Create**;
3. scegliere la subscription corretta;
4. scegliere il Resource Group:

```text
rg-obs-ud05-<codice>
```

5. impostare un nome univoco globale.

Il nome dello Storage Account deve essere:

- tutto minuscolo;
- senza trattini;
- senza spazi;
- lungo tra 3 e 24 caratteri;
- globalmente univoco.

Esempio:

```text
stobsud05mrossi01
```

Se il nome non è disponibile, aggiungere numeri finali.

Impostazioni consigliate:

| Campo | Valore consigliato |
|---|---|
| Region | stessa del Resource Group |
| Performance | Standard |
| Redundancy | Locally-redundant storage, LRS |
| Access tier | Hot, se richiesto |
| Networking | Public access, salvo diversa indicazione del docente |
| Data protection | lasciare default, salvo diversa indicazione |
| Encryption | default |

Se il Portale mostra opzioni non presenti in questa guida, mantenere i valori predefiniti, a meno che il docente indichi diversamente.

Selezionare:

```text
Review + create
Create
```

---

## 16. Abilitazione del sito statico

Aprire lo Storage Account creato.

Nel menu laterale cercare:

```text
Static website
```

Abilitare:

```text
Static website: Enabled
```

Impostare:

| Campo | Valore |
|---|---|
| Index document name | `index.html` |
| Error document path | lasciare vuoto oppure `index.html` se richiesto |

Salvare.

Dopo il salvataggio, Azure mostra un endpoint del sito statico, ad esempio:

```text
https://<nome-storage>.<area>.web.core.windows.net/
```

Annotare l’endpoint nel report.

---

## 17. Caricamento del file nel container `$web`

Quando abilitiamo lo static website, Azure crea un container speciale chiamato:

```text
$web
```

Dal menu dello Storage Account:

1. aprire **Containers**;
2. selezionare `$web`;
3. selezionare **Upload**;
4. caricare il file `index.html`;
5. confermare.

---

## 18. Verifica del sito

Aprire l’endpoint del sito statico in una nuova scheda del browser.

Dovremmo vedere la pagina HTML creata.

Se compare errore:

| Sintomo | Possibile causa |
|---|---|
| pagina 404 | `index.html` non caricato nel container `$web` |
| endpoint non disponibile | static website non abilitato o non salvato |
| pagina vecchia | cache browser, provare refresh forzato |
| accesso negato | impostazioni di accesso pubblico/rete non coerenti |

### Evidenze

Salvare:

```text
evidence/04_storage_static_website_overview.png
evidence/05_static_website_endpoint.png
```

---

## 19. Classificazione del servizio

Nel report compilare:

| Domanda | Risposta |
|---|---|
| Che cosa abbiamo creato? | Storage Account con static website |
| È IaaS, PaaS o SaaS? | PaaS |
| Gestiamo noi il sistema operativo? | No |
| Gestiamo noi un server Web? | No |
| Gestiamo noi il contenuto pubblicato? | Sì |
| Quale rischio economico resta? | Storage, traffico, eventuali configurazioni non pulite |

---

# Parte D - PaaS 2: App Service minimale

## 20. Obiettivo

Creiamo una Web App minima con Azure App Service.

Azure App Service è un servizio gestito per ospitare applicazioni Web. In questo laboratorio non distribuiamo codice applicativo complesso. Ci basta creare la risorsa e verificare la pagina iniziale generata dal servizio.

Questo serve a distinguere:

```text
Storage static website:
  contenuto statico, nessun runtime applicativo

App Service:
  piattaforma gestita per applicazioni Web con runtime
```

---

## 21. Creazione della Web App

Dal Portale:

1. cercare `App Services`;
2. selezionare **Create**;
3. scegliere **Web App**;
4. impostare la subscription corretta;
5. scegliere il Resource Group:

```text
rg-obs-ud05-<codice>
```

6. impostare un nome univoco globale.

Esempio:

```text
app-obs-ud05-mrossi
```

Se il nome non è disponibile, aggiungere numeri finali.

Impostazioni consigliate:

| Campo | Valore consigliato |
|---|---|
| Publish | Code |
| Runtime stack | Node LTS oppure Python, secondo disponibilità |
| Operating System | Linux, se disponibile |
| Region | stessa del Resource Group |
| App Service Plan | nuovo piano |
| Pricing plan | Free F1, se disponibile |

Se il piano **Free F1** non è disponibile, non scegliere piani costosi senza autorizzazione del docente. Fermarsi e annotare il problema.

Selezionare:

```text
Review + create
Create
```

---

## 22. Verifica della Web App

Dopo la creazione:

1. aprire la risorsa App Service;
2. controllare la pagina **Overview**;
3. individuare il campo **Default domain** o URL;
4. aprire l’URL nel browser.

Dovrebbe comparire una pagina iniziale/default del servizio.

Non è necessario configurare deployment, GitHub, pipeline o repository. Queste attività appartengono ad altri argomenti.

### Evidenze

Salvare:

```text
evidence/06_app_service_overview.png
evidence/07_app_service_default_page.png
```

---

## 23. Classificazione del servizio

Nel report compilare:

| Domanda | Risposta |
|---|---|
| Che cosa abbiamo creato? | Web App su Azure App Service |
| È IaaS, PaaS o SaaS? | PaaS |
| Gestiamo noi la VM sottostante? | No |
| Gestiamo noi il runtime applicativo? | In parte, scegliamo lo stack |
| Gestiamo patching dell’OS? | No, è gestito dalla piattaforma |
| Quale costo può comparire? | App Service Plan, se non gratuito |

---

# Parte E - IaaS: VM Linux minimale

## 24. Obiettivo

Creiamo o analizziamo una macchina virtuale Linux minima.

Questo è un esempio di IaaS perché Azure fornisce infrastruttura virtualizzata, ma noi dobbiamo comprendere e gestire elementi come:

- dimensione della VM;
- immagine del sistema operativo;
- disco;
- rete virtuale;
- subnet;
- interfaccia di rete;
- IP pubblico, se presente;
- Network Security Group;
- credenziali;
- stato acceso/spento;
- eliminazione delle risorse collegate.

La VM è l’attività con il rischio economico più alto della giornata. Per questo può essere svolta in tre modalità, a discrezione del docente.

| Modalità | Descrizione |
|---|---|
| Demo docente | il docente crea la VM e i partecipanti documentano |
| Lavoro a coppie | una VM ogni due partecipanti |
| Lavoro individuale | una VM per partecipante, solo se autorizzato |

Non creare VM individuali senza autorizzazione.

---

## 25. Creazione della VM

Dal Portale:

1. cercare `Virtual machines`;
2. selezionare **Create**;
3. selezionare **Azure virtual machine**;
4. scegliere la subscription corretta;
5. scegliere il Resource Group:

```text
rg-obs-ud05-<codice>
```

6. impostare un nome, ad esempio:

```text
vm-obs-ud05-<codice>
```

Impostazioni consigliate:

| Sezione | Campo | Valore consigliato |
|---|---|---|
| Basics | Region | stessa del Resource Group |
| Basics | Image | Ubuntu Server LTS |
| Basics | Size | B1s o dimensione economica autorizzata |
| Basics | Authentication | SSH public key oppure password, secondo indicazione docente |
| Basics | Public inbound ports | None, se non dobbiamo collegarci |
| Disks | OS disk type | Standard SSD o Standard HDD, secondo disponibilità |
| Networking | Virtual network | nuova o default proposta |
| Networking | Public IP | None se consentito, altrimenti default |
| Networking | NIC network security group | Basic o default |
| Management | Boot diagnostics | default |
| Monitoring | non configurare funzioni avanzate |
| Tags | tag obbligatori | corso, ud, ambiente, owner, deleteAfter |

Se il Portale propone funzionalità aggiuntive, lasciare i default o fermarsi e chiedere al docente.

Non aprire porte inutili. In questo laboratorio non dobbiamo pubblicare un server SSH o Web su Internet.

---

## 26. Verifica della VM

Dopo la creazione, aprire la pagina Overview della VM.

Osservare:

| Elemento | Che cosa indica |
|---|---|
| Status | VM running, stopped, deallocated |
| Size | potenza/costo della VM |
| Public IP address | eventuale esposizione pubblica |
| Virtual network/subnet | rete virtuale usata |
| Disk | disco OS associato |
| Network interface | scheda di rete virtuale |
| Resource Group | contenitore delle risorse |

Non è necessario collegarsi alla VM in SSH in questa UD.

### Evidenza

Salvare:

```text
evidence/08_vm_overview_o_demo.png
```

---

## 27. Spegnimento e rischio costi

Una VM accesa consuma costo compute. Una VM spenta ma non deallocata può continuare a consumare. Anche una VM deallocata può lasciare costi collegati a disco, IP pubblico o altre risorse.

La pulizia più sicura, per un laboratorio, è eliminare l’intero Resource Group alla fine, se il docente conferma che non serve più nulla.

Per ora, dopo la verifica:

1. aprire la VM;
2. selezionare **Stop**;
3. verificare che lo stato diventi **Stopped (deallocated)**, se disponibile;
4. annotare nel report.

La cancellazione finale avverrà nella fase di cleanup.

---

## 28. Classificazione del servizio

Nel report compilare:

| Domanda | Risposta |
|---|---|
| Che cosa abbiamo creato o analizzato? | Macchina virtuale Linux |
| È IaaS, PaaS o SaaS? | IaaS |
| Gestiamo il sistema operativo? | Sì, almeno logicamente |
| Gestiamo patch e configurazione OS? | Sì, se la VM resta in uso |
| Gestiamo rete e accessi? | Sì |
| Quale rischio economico resta? | Compute, disco, IP pubblico, snapshot, traffico |

---

# Parte F - SaaS: analisi guidata da Azure Marketplace

## 29. Obiettivo

Il SaaS è diverso da IaaS e PaaS.

Nel SaaS non creiamo direttamente una VM o una piattaforma applicativa da configurare. Sottoscriviamo l’uso di un software gestito da un provider. Il provider gestisce applicazione, aggiornamenti, infrastruttura sottostante e parte delle responsabilità operative.

Nel Portale Azure possiamo trovare offerte SaaS tramite Marketplace. In questa UD non acquistiamo e non sottoscriviamo offerte SaaS. Analizziamo soltanto il processo e le informazioni disponibili.

Questa cautela non è burocrazia. È sopravvivenza finanziaria con un’interfaccia grafica.

---

## 30. Esplorazione del Marketplace

Dal Portale:

1. cercare `Marketplace`;
2. aprire Azure Marketplace;
3. cercare una categoria o parola chiave, ad esempio:

```text
monitoring
backup
security
crm
project management
```

4. filtrare, se possibile, per tipo prodotto SaaS;
5. aprire una scheda prodotto;
6. leggere le informazioni principali;
7. non completare alcuna sottoscrizione.

Fermarsi prima di pulsanti come:

```text
Subscribe
Buy
Get it now
Create
Start trial
```

Se il docente decide di mostrare il flusso su un’offerta specifica, seguire solo le sue indicazioni.

---

## 31. Scheda di analisi SaaS

Nel report compilare questa tabella.

| Campo | Risposta |
|---|---|
| Nome offerta SaaS analizzata |  |
| Publisher |  |
| Categoria |  |
| Modello di prezzo visibile |  |
| Trial disponibile? |  |
| Richiede consenso/termini? |  |
| Richiede dati aziendali o account esterno? |  |
| Chi gestisce l’infrastruttura? |  |
| Chi gestisce aggiornamenti software? |  |
| Dove appare il costo? |  |
| Quali rischi di lock-in o dipendenza notiamo? |  |

### Evidenza

Salvare:

```text
evidence/09_marketplace_saas_analysis.png
```

Lo screenshot deve fermarsi alla pagina informativa dell’offerta, non a una pagina di pagamento o conferma sottoscrizione.

---

# Parte G - Confronto IaaS, PaaS, SaaS

## 32. Tabella comparativa

Nel report compilare la tabella seguente.

| Aspetto | IaaS: VM | PaaS: Storage static website | PaaS: App Service | SaaS: Marketplace |
|---|---|---|---|---|
| Che cosa usa l’utente finale? |  |  |  |  |
| Che cosa configuriamo noi? |  |  |  |  |
| Gestiamo OS? |  |  |  |  |
| Gestiamo runtime? |  |  |  |  |
| Gestiamo codice/contenuto? |  |  |  |  |
| Gestiamo rete? |  |  |  |  |
| Dove può nascere costo? |  |  |  |  |
| Chi fa patching? |  |  |  |  |
| Quanto controllo abbiamo? |  |  |  |  |
| Quanto lavoro operativo resta a noi? |  |  |  |  |

---

## 33. Lettura sintetica

Usare queste frasi come guida, poi adattarle al proprio caso.

```text
IaaS:
Azure fornisce infrastruttura virtualizzata. Noi gestiamo molto di più:
sistema operativo, patch, accessi, rete, configurazione applicativa.

PaaS:
Azure gestisce la piattaforma. Noi ci concentriamo su configurazione,
runtime, contenuto o codice applicativo.

SaaS:
Usiamo un software già gestito da un provider. Il nostro lavoro riguarda
scelta del servizio, configurazione funzionale, utenti, dati, contratto e costi.
```

---

# Parte H - Cleanup finale

## 34. Controllo delle risorse create

Aprire il Resource Group:

```text
rg-obs-ud05-<codice>
```

Verificare l’elenco delle risorse.

Possibili risorse create:

```text
Storage Account
App Service
App Service Plan
Virtual Machine
Disk
Network Interface
Network Security Group
Virtual Network
Public IP address
```

La VM spesso crea risorse collegate. Cancellare solo la VM non elimina sempre tutto ciò che è stato creato attorno.

---

## 35. Eliminazione del Resource Group

Se il docente conferma che il laboratorio è concluso e non servono più evidenze live:

1. aprire il Resource Group;
2. selezionare **Delete resource group**;
3. digitare il nome del Resource Group se richiesto;
4. confermare;
5. attendere il completamento;
6. verificare che il Resource Group non sia più presente.

Attenzione: eliminare il Resource Group cancella tutte le risorse contenute. Prima di farlo, salvare screenshot e report.

### Evidenza

Salvare:

```text
evidence/10_cleanup_finale.png
```

Se non è possibile mostrare il Resource Group eliminato, salvare uno screenshot dell’operazione di delete completata o della lista Resource Groups senza il Resource Group del laboratorio.

---

## 36. Controllo Cost Management dopo cleanup

Dopo il cleanup:

1. aprire `Cost Management + Billing`;
2. controllare la subscription;
3. verificare eventuali costi stimati o forecast;
4. annotare nel report se sono presenti anomalie.

I costi possono non aggiornarsi immediatamente. Annotare data e ora del controllo.

---

# Parte I - Report finale

## 37. File da consegnare

Compilare:

```text
docs/report_ud05_portal_iaas_paas_saas.md
```

Struttura consigliata:

```markdown
# Report UD05 - Azure Portal, IaaS, PaaS, SaaS

## 1. Dati generali

Partecipante:
Codice:
Data:
Subscription usata:
Regione usata:
Resource Group:

## 2. Orientamento nel Portale

Servizi cercati:
- Subscriptions:
- Resource groups:
- Cost Management + Billing:
- Storage accounts:
- App Services:
- Virtual machines:
- Marketplace:

Osservazioni:

## 3. Resource Group e tag

Nome Resource Group:
Regione:
Tag applicati:

Screenshot:
- evidence/02_resource_group_tags.png

## 4. Cost Management

Budget creato:
[ ] Sì
[ ] No

Motivo se non creato:

Screenshot:
- evidence/03_cost_management_budget_o_overview.png

## 5. PaaS 1 - Storage static website

Nome Storage Account:
Endpoint static website:
Risultato verifica:

Classificazione:
Perché è PaaS?

Screenshot:
- evidence/04_storage_static_website_overview.png
- evidence/05_static_website_endpoint.png

## 6. PaaS 2 - App Service

Nome App Service:
Runtime scelto:
Pricing plan:
URL:
Risultato verifica:

Classificazione:
Perché è PaaS?

Screenshot:
- evidence/06_app_service_overview.png
- evidence/07_app_service_default_page.png

## 7. IaaS - Virtual Machine

Modalità:
[ ] demo docente
[ ] coppia
[ ] individuale

Nome VM:
Sistema operativo:
Size:
Public IP presente:
Stato finale VM:

Classificazione:
Perché è IaaS?

Screenshot:
- evidence/08_vm_overview_o_demo.png

## 8. SaaS - Marketplace analysis

Nome offerta:
Publisher:
Categoria:
Trial/prezzo:
Motivi per cui è SaaS:
Rischi osservati:

Screenshot:
- evidence/09_marketplace_saas_analysis.png

## 9. Tabella comparativa

| Aspetto | IaaS: VM | PaaS: Storage static website | PaaS: App Service | SaaS: Marketplace |
|---|---|---|---|---|
| Che cosa configuriamo noi? |  |  |  |  |
| Gestiamo OS? |  |  |  |  |
| Gestiamo runtime? |  |  |  |  |
| Gestiamo rete? |  |  |  |  |
| Dove può nascere costo? |  |  |  |  |
| Quanto controllo abbiamo? |  |  |  |  |

## 10. Cleanup finale

Resource Group eliminato:
[ ] Sì
[ ] No

Risorse rimaste:
Controllo Cost Management eseguito:
Osservazioni:

Screenshot:
- evidence/10_cleanup_finale.png

## 11. Conclusioni

Differenza più chiara tra IaaS, PaaS e SaaS:

Errore o dubbio principale incontrato:

Cosa controllerei sempre prima di creare una risorsa Azure:
```

---

# Parte J - Domande di consolidamento

## 38. Domande

Rispondere nel report o in aula.

1. Perché una VM è classificata come IaaS?
2. Perché uno static website su Storage Account può essere considerato PaaS?
3. Che differenza c’è tra Storage static website e App Service?
4. Qual è il ruolo del Resource Group?
5. Perché i tag sono utili per governance e costi?
6. Qual è il rischio principale quando si crea una VM?
7. Perché in questa UD non abbiamo configurato Log Analytics o alert?
8. Perché un’offerta Marketplace SaaS non va sottoscritta alla leggera?
9. Che cosa dobbiamo controllare prima di premere **Create**?
10. Che cosa dobbiamo controllare prima di chiudere il laboratorio?

---

## 39. Risultato atteso della UD05 pratica

Alla fine del laboratorio dovremmo saper:

```text
[ ] orientarci nel Portale Azure
[ ] riconoscere subscription e Resource Group
[ ] creare un Resource Group con tag
[ ] controllare la sezione Cost Management
[ ] creare un piccolo servizio PaaS statico
[ ] creare o analizzare un App Service
[ ] creare o analizzare una VM IaaS minimale
[ ] distinguere un’offerta SaaS Marketplace da IaaS/PaaS
[ ] compilare una tabella comparativa IaaS/PaaS/SaaS
[ ] eseguire cleanup finale
[ ] documentare evidenze e decisioni operative
```

---

# Fonti ufficiali utili

Azure Portal:

```text
https://azure.microsoft.com/get-started/azure-portal
```

Resource Group da Portale:

```text
https://learn.microsoft.com/azure/azure-resource-manager/management/manage-resource-groups-portal
```

Tag da Portale:

```text
https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources-portal
```

Strategia di tagging:

```text
https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging
```

Cost Management budgets:

```text
https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets
```

Static website su Azure Storage:

```text
https://learn.microsoft.com/azure/storage/blobs/storage-blob-static-website
```

Hosting static website, guida operativa:

```text
https://learn.microsoft.com/azure/storage/blobs/storage-blob-static-website-how-to
```

Azure App Service overview:

```text
https://learn.microsoft.com/azure/app-service/overview
```

App Service quickstart Node.js:

```text
https://learn.microsoft.com/azure/app-service/quickstart-nodejs
```

Virtual machines in Azure:

```text
https://learn.microsoft.com/azure/virtual-machines
```

Creazione VM Linux da Portale:

```text
https://learn.microsoft.com/azure/virtual-machines/linux/quick-create-portal
```

Acquisto/offerte SaaS da Azure Marketplace:

```text
https://learn.microsoft.com/marketplace/purchase-saas-offer-in-azure-portal
```

Lifecycle di una subscription SaaS Marketplace:

```text
https://learn.microsoft.com/marketplace/saas-subscription-lifecycle-management
```
