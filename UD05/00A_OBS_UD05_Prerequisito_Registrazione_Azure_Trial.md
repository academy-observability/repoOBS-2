# OBS UD05 - Prerequisito: registrazione Azure Free Trial e accesso al Portale

## 1. Scopo del documento

Questo documento serve a preparare l’ambiente personale Azure prima della UD05.

Durante la UD05 lavoreremo con:

- Portale Azure;
- subscription Azure;
- Resource Group;
- tag;
- Activity Log;
- Cloud Shell;
- Azure CLI.

Per svolgere il laboratorio non basta “avere una mail Microsoft”. Serve che l’account Azure sia realmente attivo e che nel Portale sia visibile almeno una subscription utilizzabile.

---

## 2. Risultato atteso prima della lezione

Alla fine di questa preparazione dovremo essere in grado di:

1. accedere a `portal.azure.com`;
2. vedere almeno una subscription Azure attiva;
3. aprire Azure Cloud Shell in modalità Bash;
4. eseguire il comando:

```bash
az account show
```

5. visualizzare un output JSON con informazioni sulla subscription corrente;
6. sapere dove controllare costi, credito residuo e spending limit;
7. non creare risorse costose o non richieste dal laboratorio.

---

## 3. Termini minimi da chiarire prima della registrazione

### Account Microsoft o GitHub

È l’identità con cui accediamo al Portale Azure. Può essere un account Microsoft personale, ad esempio Outlook/Hotmail, oppure un account GitHub se supportato dal percorso di registrazione.

L’account di accesso non è ancora, da solo, una subscription Azure.

### Tenant o directory

Il tenant, chiamato spesso anche directory, è il contenitore di identità collegato all’account. In un contesto aziendale rappresenta l’organizzazione. In un account personale può essere creato automaticamente.

Durante la UD05 non amministriamo il tenant in profondità, ma è utile sapere che subscription e utenti sono collegati a una directory.

### Subscription

La subscription è il contenitore amministrativo e di fatturazione in cui vengono create le risorse Azure.

Senza una subscription attiva non possiamo creare Resource Group, usare molte funzioni del Portale o lavorare con Azure CLI in modo completo.

### Billing

Billing significa fatturazione. Anche se usiamo un trial, Azure richiede un profilo di fatturazione e una verifica di pagamento. Questo non significa che dobbiamo spendere denaro durante il laboratorio, ma significa che Azure deve poter identificare chi sta creando risorse cloud.

### Resource Group

Un Resource Group è un contenitore logico di risorse Azure. Nel laboratorio UD05 lo useremo per raggruppare risorse e metadati, applicare tag e leggere eventi di Activity Log.

Creare un Resource Group, di per sé, non genera normalmente costi significativi. I costi dipendono dalle risorse che vengono create dentro o collegate al Resource Group.

### Spending limit

Lo spending limit è un limite di spesa collegato al credito disponibile in alcune tipologie di account, come l’Azure free account. Serve a evitare addebiti oltre il credito previsto. Non deve essere rimosso durante il corso.

---

## 4. Cosa serve prima di iniziare

Prima di avviare la registrazione prepariamo:

| Requisito | Perché serve |
|---|---|
| Account Microsoft o GitHub | per autenticarsi al Portale Azure |
| Numero di telefono reale | per verifica tramite SMS o chiamata |
| Carta di credito o debito non prepagata | per verifica identità e profilo billing |
| Browser aggiornato | per evitare errori di sessione o cookie |
| Accesso alla propria posta elettronica | per eventuali conferme |
| Dati anagrafici coerenti con il metodo di pagamento | per ridurre errori di verifica |

Nota importante: carte prepagate, virtuali o temporanee possono essere rifiutate. Anche dati di fatturazione non coerenti con quelli registrati presso la banca possono bloccare la registrazione.

---

## 5. Percorso consigliato di registrazione Azure Free Account

### 5.1 Aprire la pagina di registrazione

Apriamo la pagina ufficiale Azure Free Account:

```text
https://azure.microsoft.com/pricing/purchase-options/azure-account
```

Da qui selezioniamo l’opzione per iniziare gratuitamente o creare un account gratuito.

La grafica del sito può cambiare, ma il percorso generale rimane:

```text
Azure Free Account
→ Start free / Try Azure for free
→ Accesso con account Microsoft o GitHub
→ Verifica identità
→ Attivazione subscription
```

---

### 5.2 Accesso con account Microsoft o GitHub

Accediamo con l’account che useremo durante il corso.

È consigliabile usare sempre lo stesso account per:

- registrazione;
- accesso al Portale;
- Cloud Shell;
- Azure CLI.

Evitare di registrarsi con un account e poi entrare nel Portale con un altro. È uno dei modi più rapidi per perdere tempo.

---

### 5.3 Compilazione del profilo

Durante la registrazione Azure può chiedere:

- nome;
- cognome;
- paese o area geografica;
- indirizzo;
- telefono;
- dati di contatto;
- dati di pagamento per verifica.

Inseriamo dati reali e coerenti. In particolare:

- il paese deve essere quello corretto;
- l’indirizzo deve essere scritto in modo plausibile e completo;
- i dati della carta devono corrispondere al titolare e all’indirizzo registrato presso la banca, quando richiesto.

---

### 5.4 Verifica tramite telefono

Azure può richiedere una verifica tramite SMS o chiamata.

Procedura tipica:

1. selezionare il prefisso paese corretto;
2. inserire il numero;
3. scegliere SMS o chiamata;
4. inserire il codice ricevuto.

Se il codice non arriva:

- attendere qualche minuto;
- controllare il prefisso internazionale;
- provare l’opzione chiamata;
- evitare numeri VoIP o temporanei;
- riprovare da browser diverso o sessione anonima.

---

### 5.5 Verifica tramite carta

Azure può chiedere una carta di credito o debito non prepagata.

Questa verifica serve a confermare l’identità e il profilo di fatturazione. Non dobbiamo interpretarla come autorizzazione a creare risorse a caso.

Durante il corso:

- non rimuoviamo lo spending limit;
- non passiamo volontariamente a piani a pagamento senza indicazione del docente;
- non creiamo risorse non previste;
- non lasciamo risorse attive se il laboratorio prevede la loro eliminazione.

---

### 5.6 Accettazione dei termini e attivazione

Al termine della procedura verrà richiesto di accettare i termini e completare la registrazione.

Dopo il completamento possono servire alcuni minuti prima che la subscription sia pienamente visibile e utilizzabile.

---

## 6. Accesso al Portale Azure

Dopo la registrazione apriamo:

```text
https://portal.azure.com
```

Effettuiamo l’accesso con lo stesso account usato per la registrazione.

Una volta entrati, verifichiamo di essere nel portale corretto e non in una pagina generica di Microsoft 365, Outlook o GitHub.

---

## 7. Verifica della subscription dal Portale

Nel Portale Azure:

1. usare la barra di ricerca in alto;
2. cercare:

```text
Subscriptions
```

3. aprire la pagina delle subscription;
4. verificare che sia presente almeno una subscription;
5. controllare che lo stato sia attivo o comunque utilizzabile.

Annotare, senza condividere pubblicamente dati sensibili:

```text
Nome subscription: ____________________________
Stato subscription: ___________________________
Tenant/directory visibile: ____________________
```

Non è necessario comunicare al docente ID completi, dati di fatturazione o informazioni personali.

---

## 8. Verifica di costi, credito e spending limit

Dal Portale Azure cercare:

```text
Cost Management + Billing
```

Verificare:

- presenza del credito trial, se disponibile;
- stato della subscription;
- eventuale spending limit;
- eventuali alert o messaggi di billing.

Indicazione per il corso:

```text
Non rimuovere lo spending limit.
Non convertire a pagamento se non strettamente necessario e consapevole.
Non creare risorse non richieste.
```

---

## 9. Apertura di Azure Cloud Shell

Azure Cloud Shell è un terminale accessibile dal browser, già autenticato e configurato per lavorare con Azure.

Dal Portale Azure:

1. selezionare l’icona di Cloud Shell nella barra superiore;
2. scegliere Bash;
3. se richiesto, selezionare la subscription;
4. se viene proposta una modalità senza storage, può essere sufficiente per verifiche rapide;
5. se viene richiesto di montare uno storage persistente, seguire le istruzioni solo se indicato dal docente.

Per la UD05 ci serve soprattutto verificare che Azure CLI funzioni.

---

## 10. Verifica Azure CLI

Dentro Cloud Shell, eseguire:

```bash
az account show
```

Output atteso: un documento JSON simile a questo:

```json
{
  "environmentName": "AzureCloud",
  "homeTenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "isDefault": true,
  "name": "Azure subscription 1",
  "state": "Enabled",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "user": {
    "name": "nomeutente@example.com",
    "type": "user"
  }
}
```

I valori reali saranno diversi.

Il campo più importante per il laboratorio è:

```json
"state": "Enabled"
```

Se lo stato non è `Enabled`, segnalare il problema al docente prima della lezione.

---

## 11. Verifica rapida della subscription da CLI

Sempre in Cloud Shell:

```bash
az account list --output table
```

Output atteso, in forma simile:

```text
Name                  CloudName    SubscriptionId                        State    IsDefault
--------------------  -----------  ------------------------------------  -------  -----------
Azure subscription 1  AzureCloud   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  Enabled  True
```

Se non compare nessuna subscription, il laboratorio UD05 non può essere svolto in modo completo da quell’account.

---

## 12. Problemi frequenti e azioni consigliate

| Problema | Possibile causa | Azione consigliata |
|---|---|---|
| Non arriva SMS | numero errato, prefisso sbagliato, blocco operatore | controllare prefisso, provare chiamata, usare numero reale |
| Carta rifiutata | carta prepagata, virtuale, dati non coerenti | usare carta supportata, controllare indirizzo billing |
| Trial non disponibile | trial già usato in passato | usare subscription esistente o valutare Pay-As-You-Go consapevolmente |
| Nel Portale non vedo subscription | account sbagliato, registrazione incompleta | uscire, rientrare con account corretto, verificare pagina Subscriptions |
| Cloud Shell non parte | subscription non attiva, provider non registrato, problema browser | provare altro browser, verificare subscription, segnalare al docente |
| `az account show` dà errore | login non valido o subscription non selezionata | chiudere e riaprire Cloud Shell, verificare account e subscription |
| Messaggi di billing | profilo incompleto o verifica non conclusa | aprire Cost Management + Billing e completare le richieste |

---

## 13. Cosa consegnare o comunicare al docente prima della UD05

Comunicare solo queste informazioni operative:

```text
[ ] Riesco ad accedere a portal.azure.com
[ ] Vedo almeno una subscription Azure
[ ] La subscription risulta Enabled/attiva
[ ] Cloud Shell Bash si apre
[ ] Il comando az account show funziona
[ ] Ho visto dove controllare Cost Management + Billing
[ ] Non ho rimosso lo spending limit
```

Non inviare:

- numero completo della carta;
- screenshot con dati di pagamento;
- ID completi se non richiesti;
- informazioni personali non necessarie.

---

## 14. Regole di sicurezza economica per il laboratorio

Durante la UD05:

1. creare solo ciò che è richiesto dal laboratorio;
2. applicare i nomi e i tag indicati;
3. controllare sempre la subscription selezionata;
4. non attivare servizi Marketplace;
5. non creare VM, database, Kubernetes, storage premium o servizi non richiesti;
6. non rimuovere spending limit;
7. eliminare eventuali risorse create se il docente lo richiede;
8. usare Cost Management per controllare eventuali costi.

---

## 15. Mini-check finale prima della lezione

Eseguire questa sequenza:

```bash
az account show --output table
```

Verificare che venga mostrato almeno:

```text
Name
State
IsDefault
```

Poi eseguire:

```bash
az group list --output table
```

Se l’account è appena stato creato, è normale che non ci siano ancora Resource Group.

L’importante è che il comando non fallisca per assenza di subscription.

---

## 16. Fonti ufficiali Microsoft da consultare

Azure Free Account:

```text
https://azure.microsoft.com/pricing/purchase-options/azure-account
```

Creazione e uso dei servizi gratuiti:

```text
https://learn.microsoft.com/azure/cost-management-billing/manage/create-free-services
```

Come evitare addebiti con Azure Free Account:

```text
https://learn.microsoft.com/azure/cost-management-billing/manage/avoid-charges-free-account
```

Spending limit:

```text
https://learn.microsoft.com/azure/cost-management-billing/manage/spending-limit
```

Problemi di registrazione:

```text
https://learn.microsoft.com/azure/cost-management-billing/troubleshoot-subscription/troubleshoot-azure-sign-up
```

Azure Cloud Shell:

```text
https://learn.microsoft.com/azure/cloud-shell/overview
```

---

## 17. Stato personale

Compilare prima della lezione:

```text
Nome partecipante: ____________________________

Account usato per il corso: ___________________

Portale Azure accessibile:
[ ] Sì
[ ] No

Subscription visibile:
[ ] Sì
[ ] No

Stato subscription:
[ ] Enabled / attiva
[ ] Altro: ___________________

Cloud Shell Bash funzionante:
[ ] Sì
[ ] No

Comando az account show funzionante:
[ ] Sì
[ ] No

Problemi riscontrati:
________________________________________________
________________________________________________
________________________________________________
```
