# OBS_UD06 - Concetti dettagliati

# Segnali diagnostici delle risorse Azure

## 1. Obiettivo della UD06

Nella UD05 abbiamo imparato a orientarci nel Portale Azure e a distinguere modelli cloud come IaaS, PaaS e SaaS.

In UD06 facciamo un passo diverso: non ci chiediamo più soltanto “che risorsa è questa?”, ma:

```text
quali segnali posso leggere?
che cosa mi dicono?
quale problema posso diagnosticare?
quale evidenza posso salvare?
```

Una risorsa cloud non è osservabile solo perché esiste. Diventa osservabile quando sappiamo trovare, interpretare e documentare i segnali che descrivono il suo comportamento.

## 2. Risorsa Azure

Una **risorsa Azure** è un oggetto gestito da Azure dentro una subscription.

Esempi:

```text
Storage Account
Virtual Machine
App Service
Public IP
Network Security Group
Virtual Network
Log Analytics Workspace
```

Una risorsa ha sempre alcune proprietà amministrative:

```text
nome
tipo
Resource Group
subscription
regione
ID univoco
tag
stato di provisioning
```

Esempio di ID risorsa:

```text
/subscriptions/<subscription-id>/resourceGroups/rg-obs-ud05-mrossi/providers/Microsoft.Web/sites/app-obs-ud05-mrossi
```

L'ID risorsa è importante perché molti comandi Azure CLI lavorano proprio su quell'identificatore.

## 3. Resource Group

Un **Resource Group** è un contenitore logico di risorse Azure.

Non è solo una cartella. Serve a:

```text
raggruppare risorse correlate
applicare tag comuni
controllare costi
gestire permessi
fare inventario
eliminare un ambiente di laboratorio in modo controllato
```

Nel nostro percorso, le risorse create in UD05 devono essere nello stesso Resource Group di laboratorio, per esempio:

```text
rg-obs-ud05-mrossi
```

In UD06 partiamo da quel Resource Group e leggiamo i segnali delle risorse che contiene.

## 4. Segnale diagnostico

Un **segnale diagnostico** è un'informazione tecnica che aiuta a capire lo stato, il comportamento o la storia operativa di una risorsa.

Esempi:

```text
la VM è accesa o deallocata?
lo Storage Account riceve richieste?
l'App Service restituisce errori?
una risorsa è stata modificata?
un Diagnostic Setting è configurato?
una metrica mostra picchi?
un log contiene eventi utili?
```

Un segnale non è automaticamente una risposta. Il segnale diventa utile quando lo colleghiamo a una domanda.

Schema:

```text
Domanda diagnostica
        |
        v
Segnale da cercare
        |
        v
Comando o pagina Portale
        |
        v
Evidenza salvata
        |
        v
Interpretazione tecnica
```

Esempio:

```text
Domanda:
La VM sta generando costo compute?

Segnale:
Power state della VM.

Comando:
az vm get-instance-view

Interpretazione:
Se la VM è running consuma compute.
Se è stopped/deallocated non consuma compute, ma possono restare costi di disco, IP, snapshot.
```

## 5. Risorsa osservabile

Una **risorsa osservabile** è una risorsa per cui sappiamo individuare e leggere segnali utili.

Non basta dire:

```text
Ho creato una VM.
```

In UD06 dobbiamo arrivare a dire:

```text
La VM è nello stato running.
Ha una dimensione B1s.
Ha un disco OS associato.
Ha una scheda di rete.
Ha o non ha IP pubblico.
Espone metriche CPU, disco e rete.
Ha o non ha boot diagnostics.
Il suo Activity Log mostra gli eventi amministrativi recenti.
```

Questa è una lettura osservabile della risorsa.

## 6. Stato amministrativo e stato operativo

Lo **stato amministrativo** riguarda la gestione della risorsa da parte di Azure.

Esempi:

```text
provisioning succeeded
resource created
resource updated
resource deleted
tag changed
```

Lo **stato operativo** riguarda il funzionamento della risorsa.

Esempi:

```text
VM running
VM stopped
App Service started
App Service stopped
Storage Account reachable
endpoint HTTP raggiungibile
```

Schema:

```text
Risorsa Azure
  |
  +-- Stato amministrativo
  |     +-- creata?
  |     +-- modificata?
  |     +-- da chi?
  |     +-- quando?
  |
  +-- Stato operativo
        +-- accesa?
        +-- raggiungibile?
        +-- risponde?
        +-- consuma risorse?
```

In un report diagnostico dobbiamo evitare frasi generiche come:

```text
La risorsa sembra ok.
```

Meglio:

```text
La risorsa esiste nel Resource Group indicato, ha provisioningState Succeeded e l'App Service risulta in stato Running.
```

## 7. Activity Log

L'**Activity Log** è il log amministrativo della subscription Azure.

Registra eventi come:

```text
creazione risorsa
modifica risorsa
eliminazione risorsa
avvio/arresto VM
modifica tag
modifica configurazione
errore amministrativo
```

L'Activity Log risponde a domande come:

```text
Chi ha modificato questa risorsa?
Quando è stata creata?
Quale operazione è fallita?
Sono stati cambiati i tag?
È stata avviata o fermata una VM?
```

L'Activity Log non risponde bene a domande applicative come:

```text
Quante richieste HTTP hanno dato 500?
Qual è la latenza p95 dell'applicazione?
Quale utente ha chiamato l'endpoint /checkout?
```

Quelle domande richiedono log applicativi, metriche applicative o strumenti successivi.

## 8. Metrica

Una **metrica** è un valore numerico misurato nel tempo.

Esempi:

```text
CPU Percentage
Memory usage
Requests
Response time
Transactions
Ingress
Egress
Availability
Disk read/write
Network in/out
```

Una metrica ha almeno:

```text
nome
valore
timestamp
unita di misura
aggregazione
periodo temporale
```

Esempio:

```text
Nome metrica: Percentage CPU
Valore: 14.2
Unita: Percent
Timestamp: 2026-06-28T10:15:00Z
Aggregazione: Average
Time range: ultimi 30 minuti
```

Schema:

```text
tempo  -----> 10:00   10:05   10:10   10:15
CPU %          12      18      80      15
```

Una metrica è utile per vedere andamento, picchi, soglie e anomalie quantitative.

## 9. Aggregazione

Un'**aggregazione** è il modo in cui più valori vengono sintetizzati in un intervallo temporale.

Esempi:

```text
Average = media
Minimum = valore minimo
Maximum = valore massimo
Total = somma
Count = conteggio
```

Esempio:

```text
Valori CPU in 5 minuti:
10, 12, 90, 11, 10

Average = 26.6
Maximum = 90
```

La media nasconde il picco. Il massimo lo evidenzia.

Per questo, quando analizziamo una metrica, dobbiamo sempre indicare:

```text
quale metrica
quale time range
quale aggregazione
quale granularità
```

## 10. Time range e granularità

Il **time range** è l'intervallo temporale analizzato.

Esempi:

```text
ultimi 30 minuti
ultima ora
ultime 24 ore
giornata di laboratorio
```

La **granularità** è la dimensione dei blocchi temporali usati per aggregare i dati.

Esempi:

```text
1 minuto
5 minuti
15 minuti
1 ora
```

Schema:

```text
Time range: ultima ora

Granularità 5 minuti:
[10:00-10:05] [10:05-10:10] [10:10-10:15] ...

Granularità 30 minuti:
[10:00-10:30] [10:30-11:00]
```

Un grafico senza time range e senza aggregazione è ambiguo.

## 11. Log

Un **log** è una sequenza di eventi.

Un evento di log descrive qualcosa che è successo.

Esempi:

```text
richiesta HTTP ricevuta
errore applicativo
deployment completato
avvio servizio
connessione rifiutata
operazione amministrativa fallita
```

Un log può essere:

```text
amministrativo
di risorsa
applicativo
di sistema operativo
di sicurezza
```

Differenza sintetica:

```text
Metrica = numero nel tempo
Log     = evento con dettagli
```

Esempio:

```text
Metrica:
Requests = 120 nell'ultimo minuto

Log:
2026-06-28T10:15:01Z GET /api/orders 500 request_id=abc123 duration_ms=842
```

## 12. Resource Log

Un **Resource Log** è un log prodotto da una specifica risorsa Azure.

Esempi:

```text
log di accesso di un App Service
log diagnostici di Storage Account
log di un Key Vault
log di un Application Gateway
```

I Resource Log non arrivano automaticamente in Log Analytics. Di solito serve un Diagnostic Setting.

Questa distinzione è importante:

```text
La risorsa può produrre log
ma quei log non sono necessariamente raccolti
```

## 13. Diagnostic Setting

Un **Diagnostic Setting** è una configurazione che invia log e/o metriche di una risorsa verso una destinazione.

Destinazioni tipiche:

```text
Log Analytics Workspace
Storage Account
Event Hub
partner solution
```

Schema:

```text
Risorsa Azure
  |
  +-- Metriche
  +-- Resource Log
         |
         v
Diagnostic Setting
         |
         +-- Log Analytics Workspace
         +-- Storage Account
         +-- Event Hub
```

In UD06 ci interessa soprattutto verificare:

```text
la risorsa supporta Diagnostic Settings?
quali categorie diagnostiche sono disponibili?
esiste già un Diagnostic Setting?
verso quale destinazione invia i dati?
```

La configurazione approfondita sarà ripresa in UD07.

## 14. Categoria diagnostica

Una **categoria diagnostica** è un tipo di log o metrica esportabile tramite Diagnostic Settings.

Esempi possibili:

```text
AuditEvent
AppServiceHTTPLogs
AppServiceConsoleLogs
StorageRead
StorageWrite
StorageDelete
```

Le categorie non sono uguali per tutte le risorse.

Uno Storage Account, una VM e un App Service espongono segnali diversi perché sono servizi diversi.

Schema:

```text
Storage Account
  +-- transazioni
  +-- ingress/egress
  +-- categorie legate ai servizi blob/file/queue/table

App Service
  +-- richieste HTTP
  +-- stato applicazione
  +-- log applicativi, se abilitati

Virtual Machine
  +-- stato power
  +-- CPU
  +-- disco
  +-- rete
  +-- boot diagnostics
```

## 15. Storage Account come risorsa osservabile

Uno **Storage Account** è un servizio Azure per archiviazione dati.

In UD05 può essere stato usato anche per pubblicare uno static website.

In UD06 non lo ricreiamo. Lo osserviamo.

Domande diagnostiche tipiche:

```text
Lo Storage Account esiste nel Resource Group atteso?
Quale endpoint espone?
Ha traffico recente?
Ci sono transazioni?
Quali metriche sono disponibili?
Supporta Diagnostic Settings?
Quali categorie diagnostiche sono disponibili per Blob?
```

Esempi di segnali:

```text
resource details
endpoint static website
metric definitions
Transactions
Ingress
Egress
Availability
diagnostic categories
diagnostic settings
Activity Log
```

## 16. Virtual Machine come risorsa osservabile

Una **Virtual Machine** Azure è una macchina virtuale gestita come risorsa IaaS.

Termini minimi:

```text
VM = macchina virtuale
OS = sistema operativo installato nella VM
disk = disco associato alla VM
NIC = scheda di rete virtuale
NSG = Network Security Group, cioè regole di traffico di rete
Public IP = indirizzo IP pubblico, se assegnato
power state = stato acceso/spento/deallocato
```

In UD06 non usiamo la VM per imparare Linux. La usiamo per leggere segnali cloud.

Domande diagnostiche tipiche:

```text
La VM è running o deallocated?
Ha IP pubblico?
Quale dimensione usa?
Ha boot diagnostics?
Quali metriche espone?
Ci sono eventi recenti di start/stop?
Ci sono risorse collegate che possono generare costo?
```

Esempi di segnali:

```text
powerState
vmSize
networkProfile
storageProfile
bootDiagnostics
Percentage CPU
Network In/Out
Disk Read/Write
Activity Log
```

## 17. App Service come risorsa osservabile

Un **App Service** è un servizio PaaS per ospitare applicazioni Web.

Termini minimi:

```text
Web App = applicazione ospitata su App Service
App Service Plan = piano che definisce risorse/costo dell'hosting
runtime = ambiente che esegue il codice, ad esempio Python o Node
default hostname = dominio assegnato da Azure
```

In UD06 non facciamo deployment applicativo. Osserviamo la risorsa.

Domande diagnostiche tipiche:

```text
La Web App è running?
Quale hostname espone?
Quale runtime o stack usa?
Quale App Service Plan la ospita?
Quali metriche espone?
I log applicativi sono abilitati?
Quali categorie diagnostiche sono disponibili?
```

Esempi di segnali:

```text
state
defaultHostName
serverFarmId
siteConfig
Requests
Http 5xx
Average Response Time
diagnostic categories
diagnostic settings
Activity Log
```

## 18. CLI e Portale

In UD06 usiamo sia Portale Azure sia Azure CLI.

Il **Portale Azure** è utile per:

```text
orientarsi visivamente
aprire Overview
vedere grafici rapidi
ispezionare Activity Log
controllare Diagnostic Settings
```

La **Azure CLI** è utile per:

```text
salvare output ripetibili
creare evidenze JSON
verificare resource id
estrarre inventario
documentare comandi esatti
```

Una buona evidenza tecnica non è solo uno screenshot. È un output che può essere riletto e confrontato.

## 19. JSON come formato di evidenza

Molti comandi Azure CLI producono output JSON.

**JSON** significa JavaScript Object Notation. In pratica è un formato testuale strutturato composto da:

```text
oggetti
coppie chiave/valore
liste
stringhe
numeri
booleani
null
```

Esempio:

```json
{
  "name": "app-obs-ud05-mrossi",
  "state": "Running",
  "defaultHostName": "app-obs-ud05-mrossi.azurewebsites.net"
}
```

Il JSON è utile perché può essere:

```text
letto da persone
salvato come evidenza
elaborato da script
confrontato nel tempo
usato in automazioni
```

## 20. Metodo diagnostico UD06

Ogni analisi deve seguire questo schema:

```text
1. Identifico la risorsa.
2. Recupero il suo Resource ID.
3. Verifico lo stato amministrativo.
4. Verifico lo stato operativo.
5. Cerco metriche disponibili.
6. Leggo alcuni valori metrici recenti.
7. Controllo Diagnostic Settings e categorie disponibili.
8. Cerco eventi Activity Log recenti.
9. Salvo evidenze.
10. Scrivo interpretazione tecnica.
```

Non basta raccogliere output.

Esempio di interpretazione debole:

```text
Ho visto le metriche della VM.
```

Esempio di interpretazione accettabile:

```text
La VM espone metriche CPU, disco e rete. Nel time range analizzato non risultano valori significativi perché la VM era deallocata. Questo è coerente con il powerState rilevato.
```

## 21. Errori concettuali da evitare

| Errore | Correzione |
|---|---|
| Confondere Activity Log e log applicativi | Activity Log = operazioni Azure; log applicativi = eventi prodotti dall'app |
| Dire che una risorsa “non ha log” senza verificare Diagnostic Settings | Prima verificare categorie disponibili e configurazioni esistenti |
| Guardare una metrica senza time range | Ogni metrica richiede intervallo temporale e aggregazione |
| Considerare uno screenshot come unica evidenza | Preferire output JSON/CLI quando possibile |
| Pensare che creare una risorsa equivalga a osservarla | Osservare significa leggere segnali e interpretarli |
| Dimenticare i costi residui | Anche risorse ferme possono lasciare dischi, IP o piani a costo |

## 22. Mappa finale dei segnali

```text
Risorsa Azure
  |
  +-- Identità e governance
  |     +-- nome
  |     +-- tipo
  |     +-- Resource Group
  |     +-- tag
  |
  +-- Stato
  |     +-- provisioningState
  |     +-- powerState / running / stopped
  |
  +-- Activity Log
  |     +-- create
  |     +-- update
  |     +-- delete
  |     +-- start/stop
  |
  +-- Metriche
  |     +-- valori numerici nel tempo
  |     +-- aggregazioni
  |     +-- time range
  |
  +-- Log di risorsa
  |     +-- categorie disponibili
  |     +-- raccolta tramite Diagnostic Settings
  |
  +-- Evidenze
        +-- JSON
        +-- screenshot mirati
        +-- report tecnico
```

## 23. Risultato atteso

Alla fine della UD06 dobbiamo saper prendere una risorsa creata in UD05 e produrre una diagnosi minima:

```text
risorsa identificata
stato rilevato
segnali disponibili
metriche disponibili
eventi amministrativi recenti
diagnostic settings verificati
evidenze salvate
interpretazione tecnica
azione consigliata
```

Questa capacità prepara UD07, dove entreremo più in dettaglio su Azure Monitor, metriche e Diagnostic Settings.

