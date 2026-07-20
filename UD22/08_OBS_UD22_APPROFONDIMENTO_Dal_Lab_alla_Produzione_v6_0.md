# OBS UD22 — Approfondimento
# Dal laboratorio a un'architettura Jaeger di produzione

## 1. Perché il laboratorio usa all-in-one e Badger

L'ambiente locale privilegia:

- avvio rapido;
- consumo contenuto di risorse;
- un solo nodo;
- comportamento ripetibile;
- visibilità diretta di collector, storage, query e UI.

Badger è embedded e non richiede un database esterno. È adatto a questa finalità, ma non rappresenta automaticamente la scelta corretta per un sistema distribuito ad alto volume.

## 2. Evoluzione concettuale

```text
Laboratorio
app -> Jaeger all-in-one -> Badger locale

Produzione
app -> OpenTelemetry Collector -> Jaeger Collector -> storage distribuito
                                      Jaeger Query -> storage distribuito
```

In un'architettura reale diventano rilevanti:

- alta disponibilità dei collector;
- bilanciamento;
- autenticazione e TLS;
- capacità e prestazioni dello storage;
- retention;
- sampling;
- controllo dei costi;
- segregazione degli ambienti;
- sicurezza degli attributi e dei dati sensibili.

## 3. Backend distribuiti

Jaeger può utilizzare storage esterni, per esempio OpenSearch/Elasticsearch o Cassandra. La selezione dipende da scala, competenze del team, requisiti di retention, costi e modello operativo.

L'obiettivo della UD non è amministrare questi sistemi, ma comprendere che la UI Jaeger interroga uno storage e che la qualità del servizio di tracing dipende anche dalla sua architettura.

## 4. OpenTelemetry Collector

In produzione è frequente inserire uno o più OpenTelemetry Collector tra applicazioni e backend:

```text
applicazioni -> OTel Collector -> Jaeger o altro backend
```

Il collector può ricevere, trasformare, filtrare, campionare e inoltrare telemetria. Questa separazione riduce il legame diretto tra applicazioni e specifico backend.

## 5. Competenza da portare con sé

Il partecipante non deve memorizzare una topologia unica. Deve saper riconoscere le responsabilità:

```text
strumentazione
propagazione
raccolta
sampling
storage
query e visualizzazione
retention
```

## 6. Nota sulla versione dello stack

Il laboratorio fissa l'immagine `jaegertracing/all-in-one:1.76.0` per mantenere stabile la configurazione Badger e rendere ripetibili le attività. Per un nuovo progetto produttivo occorre verificare la release corrente di Jaeger, le relative architetture supportate e l'eventuale percorso di migrazione.
