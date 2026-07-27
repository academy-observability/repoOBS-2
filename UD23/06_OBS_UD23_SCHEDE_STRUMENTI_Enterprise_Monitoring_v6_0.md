# OBS UD23 - Schede strumenti
# Enterprise monitoring e observability: casi d'uso pronti per la comparativa

## 0. Come usare questo file

Questo file evita che la comparativa sugli strumenti venga lasciata all'improvvisazione. Gli strumenti qui descritti non richiedono installazioni enterprise nel laboratorio UD23. Zabbix, Splunk e OpenText vengono trattati tramite schede operative e casi d'uso; **Dynatrace viene anche esplorato praticamente tramite Playground**.

Regola:

```text
Se non abbiamo usato direttamente lo strumento, nel report scriviamo:
"valutazione basata su scheda e caso d'uso".

Per Dynatrace distinguiamo:

```text
esplorazione pratica in Playground = sì
installazione/configurazione OneAgent = non svolta nel percorso core
```
```

## 1. Elastic / Kibana

### Posizionamento

Elastic/Kibana viene spesso usato per indicizzare, cercare, filtrare e visualizzare log o eventi. Kibana consente dashboard e interrogazioni sui dati indicizzati in Elasticsearch.

### Caso d'uso adatto

```text
Il team deve cercare rapidamente errori applicativi su grandi volumi di log JSON,
filtrando per servizio, endpoint, status code, request_id e intervallo temporale.
```

### Segnali forti

- log search;
- filtri per campo;
- dashboard log;
- pattern di errore;
- analisi testuale.

### Limiti da considerare

- gestione ingestion e mapping;
- retention e costi storage;
- gestione cluster se self-managed;
- non sostituisce automaticamente APM o tracing.

### Esercizio guidato senza installazione

Usiamo il dataset:

```text
UD23/data/logs/products_logs_sample.jsonl
```

Domanda:

```text
Quali endpoint generano più errori 5xx?
```

Usa lo script `query_logs.py` e riporta risultato nel report.

## 2. Zabbix

### Posizionamento

Zabbix è forte nel monitoraggio infrastrutturale tradizionale: host, item, trigger, availability, servizi e dispositivi.

### Caso d'uso adatto

```text
Una azienda ha server, VM, apparati o servizi legacy e vuole trigger su disponibilità,
CPU, memoria, disco, processi o porte.
```

### Segnali forti

- host monitoring;
- item;
- trigger;
- availability;
- infrastruttura tradizionale.

### Limiti da considerare

- meno centrato su APM moderno rispetto a strumenti dedicati;
- richiede modellazione di host/item/trigger;
- non è il primo strumento da scegliere per tracing distribuito FE -> BE.

### Mini-caso

Scenario:

```text
Il backend products gira su una VM legacy e ogni tanto il processo si ferma.
```

Domanda:

```text
Zabbix è adatto? Quale trigger configureresti concettualmente?
```

Risposta attesa:

```text
Sì, se il problema riguarda disponibilità del processo/host/porta.
Trigger candidato: servizio non raggiungibile o porta non in ascolto per più di N minuti.
```

## 3. Splunk

### Posizionamento

Splunk è molto usato in ambienti enterprise per indicizzare, cercare e correlare grandi volumi di dati macchina. Nella famiglia Splunk Observability rientrano anche metriche, eventi, log e APM.

### Caso d'uso adatto

```text
L'azienda ha molte fonti log eterogenee, necessita retention, ricerche avanzate,
correlazioni e dashboard per security/operations/business.
```

### Segnali forti

- log search enterprise;
- correlazione eventi;
- dashboard;
- integrazione con processi aziendali;
- APM nella piattaforma observability.

### Limiti da considerare

- costo/licensing;
- governance ingestion;
- necessità di progettare indici e retention;
- curva di apprendimento.

### Mini-caso

Scenario:

```text
Il team deve correlare errori dell'app products con log di gateway, firewall e autenticazione.
```

Splunk è candidato perché gestisce bene fonti eterogenee e ricerca/correlazione log enterprise.

## 4. Dynatrace

### Posizionamento

Dynatrace è una piattaforma enterprise di observability/APM orientata a monitorare applicazioni distribuite, dipendenze, tracing, infrastruttura e user experience.

### Caso d'uso adatto

```text
Un'organizzazione complessa vuole service map, distributed tracing, APM avanzato,
automatic discovery e analisi su molte applicazioni distribuite.
```

### Segnali forti

- APM;
- distributed tracing;
- service flow;
- dependency map;
- user experience;
- automazione/AI di supporto all'analisi.

### Limiti da considerare

- costo;
- complessità;
- rischio di sovradimensionamento per team piccoli;
- dipendenza da piattaforma enterprise.

### Mini-caso

Scenario:

```text
Il catalogo prodotti è solo una piccola parte di un ecosistema con decine di microservizi.
Serve capire automaticamente le dipendenze e l'impatto utente.
```

Dynatrace diventa candidato più credibile rispetto a una soluzione minimale manuale.

### Attività pratica associata

Apri `10_OBS_UD23_DEMO_GUIDATA_Dynatrace_Playground_v6_0.md`. La demo richiede di osservare almeno un servizio, endpoint, metriche di salute, infrastruttura, log o trace e una relazione tra servizi. Non richiede installazione OneAgent.

## 5. OpenText AI Operations Management / Operations Bridge

### Posizionamento

OpenText Operations Bridge rientra nel mondo ITOM/AIOps enterprise: consolidamento eventi, monitoraggio, automazione, correlazione e riduzione del rumore operativo in ambienti ibridi/multicloud.

### Caso d'uso adatto

```text
Una grande organizzazione vuole unificare eventi, monitoraggio e automazione operativa
su ambienti multicloud, on-premises e processi ITSM.
```

### Segnali forti

- AIOps/ITOM;
- correlazione eventi;
- automazione remediation;
- riduzione rumore;
- governance enterprise.

### Limiti da considerare

- non è uno strumento da introdurre per un piccolo laboratorio applicativo;
- richiede contesto enterprise e integrazione con processi esistenti;
- valutazione più organizzativa che puramente tecnica.

### Mini-caso

Scenario:

```text
L'azienda riceve migliaia di eventi da cloud, rete, server, applicazioni e service desk.
Serve correlare eventi e ridurre alert noise.
```

OpenText è più pertinente come piattaforma IT operations/AIOps che come semplice dashboard applicativa.

## 6. Tabella di sintesi pronta

| Strumento | Più adatto per | Meno adatto per | Valutazione nel lab |
|---|---|---|---|
| Prometheus/Grafana | metriche, dashboard, alert | log search avanzato | provato direttamente |
| Application Insights/Azure Monitor | APM cloud Azure, richieste, dipendenze | ambienti non Azure senza integrazioni | provato direttamente |
| Log Analytics/KQL | query log/cloud telemetry | dashboard UX avanzata da sola | provato direttamente |
| Elastic/Kibana | log search e dashboard log | tracing/APM completo senza componenti aggiuntivi | simulato con dataset |
| Zabbix | host/service/trigger | APM cloud-native profondo | scheda/caso d'uso |
| Splunk | log/eventi enterprise, correlazione | soluzione low-cost per piccoli team | scheda/caso d'uso |
| Dynatrace | APM enterprise e distributed tracing | contesti piccoli con budget limitato | **provato in Playground + scheda** |
| OpenText | ITOM/AIOps enterprise | laboratorio applicativo minimale | scheda/caso d'uso |
