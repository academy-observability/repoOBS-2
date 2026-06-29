# OBS_UD05 - Concetti

# Azure Portal, IaaS, PaaS, SaaS e preparazione della UD06

## 1. Punto di partenza

Prima di questa UD i partecipanti hanno gia studiato:

```text
CloudComputingIntro.pdf
00A_OBS_UD05_Prerequisito_Registrazione_Azure_Trial.md
00B_OBS_UD05_LAB_pratico_Azure_Portal_IaaS_PaaS_SaaS.md
```

Questa UD non ripete tutto il materiale teorico. Lo riorganizza in una atività pratica con un vincolo preciso:

```text
le risorse create oggi saranno usate domani nella UD06.
```

Quindi l'obiettivo non e solo “creare qualcosa su Azure”, ma creare risorse riconoscibili, documentate, taggate e mantenute disponibili per l'analisi dei segnali diagnostici.

## 2. Azure Portal

**Azure Portal** è l'interfaccia Web per gestire risorse Azure.

Serve per:

```text
creare risorse
consultare subscription e Resource Group
vedere costi e budget
aprire Overview delle risorse
controllare Activity Log
raggiungere pannelli di monitoraggio e diagnostica
```

In UD05 usiamo il Portale per orientarci e creare risorse semplici.

In UD06 useremo le stesse risorse per leggere segnali diagnostici.

## 3. Tenant, subscription e Resource Group

Un **tenant** rappresenta il contesto di identita Microsoft Entra ID.

Una **subscription** rappresenta il contenitore amministrativo e di fatturazione dove vengono create risorse Azure.

Un **Resource Group** è un contenitore logico di risorse.

Schema:

```text
Tenant
  |
  +-- Subscription
        |
        +-- Resource Group
              |
              +-- Storage Account
              +-- App Service
              +-- Virtual Machine
              +-- Virtual Network
              +-- Disk
              +-- Public IP
```

In UD05 lavoriamo dentro un Resource Group di laboratorio, per esempio:

```text
rg-obs-ud05-mrossi
```

Questo Resource Group non deve essere eliminato alla fine della giornata, perchè servirà in UD06.

## 4. Risorsa Azure

Una **risorsa Azure** è un oggetto creato e gestito dentro Azure.

Esempi:

```text
Storage Account
App Service
Virtual Machine
Disk
Network Interface
Network Security Group
Virtual Network
Public IP
```

Ogni risorsa ha:

```text
nome
tipo
regione
Resource Group
Resource ID
stato
configurazione
eventuali costi
eventuali segnali diagnostici
```

UD05 crea e classifica risorse.

UD06 legge i loro segnali.

## 5. Regione

La **regione** è l'area geografica Azure dove viene ospitata una risorsa.

Esempi:

```text
West Europe
North Europe
Italy North
France Central
```

Non tutte le regioni offrono sempre gli stessi servizi, SKU o prezzi.

In un laboratorio è consigliabile usare una sola regione per ridurre confusione e dispersione.

## 6. Naming convention

Una **naming convention** è una regola condivisa per nominare risorse.

Esempi:

```text
rg-obs-ud05-mrossi
stobsud05mrossi01
app-obs-ud05-mrossi
vm-obs-ud05-mrossi
```

Perchè serve:

```text
riconoscere le risorse
evitare nomi casuali
semplificare inventario
semplificare cleanup futuro
collegare risorse a corso, UD e partecipante
```

Alcune risorse, come Storage Account e App Service, richiedono nomi globalmente univoci.

## 7. Tag

Un **tag** è un metadato chiave-valore associato a una risorsa.

Esempi:

```text
corso=observability
ud=05
ambiente=lab
owner=mrossi
deleteAfter=2026-06-30
```

I tag servono a:

```text
identificare proprietario
classificare ambiente
controllare costi
semplificare governance
supportare cleanup
filtrare risorse
```

In questa UD i tag non sono opzionali.

## 8. Cost Management

**Cost Management** è l'area Azure usata per osservare costi, forecast, budget e scope di fatturazione.

Prima di creare risorse dobbiamo verificare:

```text
subscription corretta
spending limit, se presente
budget o overview costi
SKU scelte
risorse che possono generare costo continuativo
```

La VM è il servizio piu delicato: se resta accesa, puo generare costo compute.

Per questo, a fine UD05, la VM puo essere fermata/deallocata se il docente lo richiede.

Non va però eliminata, perchè deve restare analizzabile in UD06.

## 9. IaaS

**IaaS** significa Infrastructure as a Service.

Azure fornisce infrastruttura virtualizzata. Noi gestiamo piu dettagli operativi.

Esempio UD05:

```text
Virtual Machine Linux
```

Con una VM dobbiamo considerare:

```text
sistema operativo
dimensione
disco
rete
IP pubblico
NSG
stato running/stopped/deallocated
costo compute
```

In UD05 la VM serve a capire il modello IaaS.

In UD06 la stessa VM servira per leggere segnali come stato, metriche CPU/rete/disco, Activity Log e risorse collegate.

## 10. PaaS

**PaaS** significa Platform as a Service.

Azure gestisce la piattaforma sottostante. Noi configuriamo servizio, runtime, contenuto o codice.

Esempi UD05:

```text
Storage Account con static website
App Service minimale
```

Differenza:

```text
Storage static website:
  contenuto statico, nessun runtime applicativo da gestire

App Service:
  hosting gestito per applicazioni Web con runtime
```

In UD06 osserveremo metriche, stato e configurazioni diagnostiche di queste risorse.

## 11. SaaS

**SaaS** significa Software as a Service.

Non creiamo infrastruttura e non gestiamo piattaforma applicativa. Usiamo un software gestito da un provider.

In UD05 non acquistiamo e non sottoscriviamo servizi SaaS.

Facciamo solo analisi Marketplace:

```text
nome offerta
publisher
categoria
modello prezzo
trial
permessi richiesti
rischi di lock-in
responsabilita operative
```

Regola:

```text
fermarsi prima di Subscribe, Buy, Get it now, Create o Start trial.
```

## 12. Activity Log

L'**Activity Log** registra operazioni amministrative su Azure.

Esempi:

```text
creazione Resource Group
creazione App Service
aggiornamento tag
avvio VM
arresto VM
eliminazione risorsa
errore di deploy
```

In UD05 lo usiamo solo come primo controllo.

In UD06 diventerà una fonte diagnostica da leggere in modo piu strutturato.

## 13. Perche non eliminiamo le risorse

Questa e la regola centrale della nuova sequenza UD05-UD06.

Alla fine di UD05 le risorse devono restare disponibili per la UD06.

```text
UD05:
crea, classifica, documenta, controlla costi

UD06:
osserva, misura, legge segnali, interpreta
```

Se eliminiamo tutto alla fine della UD05, la UD06 perde il contesto reale.

Sono consentite solo azioni conservative:

```text
fermare/deallocare la VM se richiesto
verificare costi
salvare evidenze
annotare cosa resta attivo
```

Attenzione quindi a:

```text
eliminare Resource Group
eliminare Storage Account
eliminare App Service
eliminare VM
eliminare dischi, IP o rete collegati
```

## 14. Risultato atteso

Alla fine della UD05 ogni partecipante deve poter dire:

```text
Ho identificato la subscription.
Ho creato o verificato un Resource Group taggato.
Ho controllato Cost Management.
Ho creato almeno un esempio PaaS statico.
Ho creato o analizzato un App Service.
Ho creato o analizzato una VM IaaS controllata.
Ho analizzato un'offerta SaaS senza sottoscriverla.
Ho compilato una tabella IaaS/PaaS/SaaS.
Ho lasciato le risorse disponibili per UD06.
Ho salvato un inventario utile alla diagnosi successiva.
```

