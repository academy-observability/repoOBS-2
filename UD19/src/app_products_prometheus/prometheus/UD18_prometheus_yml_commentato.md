# Configurazione Prometheus commentata

Di seguito è riportato il file `prometheus.yml` utilizzato nel laboratorio UD18, arricchito con commenti dettagliati.

I commenti YAML iniziano con `#` e vengono ignorati da Prometheus durante il caricamento della configurazione.

```yaml
# ============================================================
# CONFIGURAZIONE GENERALE DI PROMETHEUS
# ============================================================

global:

  # Intervallo con cui Prometheus interroga tutti i target.
  #
  # Ogni 10 secondi Prometheus esegue una richiesta HTTP
  # verso l'endpoint delle metriche di ciascun servizio.
  #
  # Esempi:
  #   http://backend-products:8000/metrics
  #   http://frontend-products:8080/metrics
  #   http://localhost:9090/metrics
  #
  # Questo valore può essere ridefinito all'interno di un
  # singolo job, qualora un target richieda una frequenza diversa.
  scrape_interval: 10s

  # Intervallo con cui Prometheus valuta le regole configurate.
  #
  # Le regole possono essere:
  # - alerting rules, utilizzate per generare allarmi;
  # - recording rules, utilizzate per precalcolare query PromQL.
  #
  # Questo parametro non riguarda la raccolta delle metriche,
  # ma la frequenza di valutazione delle regole sui dati raccolti.
  evaluation_interval: 10s


# ============================================================
# CONFIGURAZIONE DEI TARGET DA MONITORARE
# ============================================================

# La sezione scrape_configs contiene l'elenco dei job.
#
# Ogni job identifica uno o più target dai quali Prometheus
# deve raccogliere le metriche.
scrape_configs:

  # ----------------------------------------------------------
  # JOB 1: BACKEND DEL CATALOGO PRODOTTI
  # ----------------------------------------------------------

  # Nome logico assegnato al job del backend.
  #
  # Questo nome viene aggiunto automaticamente alle metriche
  # raccolte tramite la label:
  #
  #   job="products-backend"
  #
  # Esempio:
  #
  #   up{
  #     job="products-backend",
  #     instance="backend-products:8000"
  #   }
  - job_name: "products-backend"

    # Percorso HTTP esposto dall'applicazione backend
    # per pubblicare le metriche nel formato Prometheus.
    #
    # Prometheus costruirà l'URL completo combinando:
    #
    #   target       = backend-products:8000
    #   metrics_path = /metrics
    #
    # URL risultante:
    #
    #   http://backend-products:8000/metrics
    metrics_path: /metrics

    # static_configs indica che i target sono dichiarati
    # manualmente all'interno di questo file.
    #
    # Non viene quindi utilizzato un sistema automatico
    # di service discovery, come Kubernetes, Azure o Consul.
    static_configs:

      # Elenco degli indirizzi da interrogare per questo job.
      #
      # backend-products è il nome DNS del servizio Docker.
      # In una rete Docker Compose, il nome del servizio può
      # essere utilizzato come hostname dagli altri container.
      #
      # 8000 è la porta interna sulla quale il backend Flask
      # ascolta le richieste HTTP.
      #
      # Prometheus deve trovarsi nella stessa rete Docker
      # del servizio backend-products.
      - targets: ["backend-products:8000"]


  # ----------------------------------------------------------
  # JOB 2: FRONTEND DEL CATALOGO PRODOTTI
  # ----------------------------------------------------------

  # Nome logico assegnato al job del frontend.
  #
  # Le metriche raccolte da questo target avranno la label:
  #
  #   job="products-frontend"
  #
  # Esempio:
  #
  #   up{
  #     job="products-frontend",
  #     instance="frontend-products:8080"
  #   }
  - job_name: "products-frontend"

    # Percorso HTTP dal quale Prometheus raccoglie
    # le metriche pubblicate dal frontend.
    #
    # URL completo:
    #
    #   http://frontend-products:8080/metrics
    metrics_path: /metrics

    # Anche il frontend viene configurato tramite
    # una dichiarazione statica del target.
    static_configs:

      # frontend-products è il nome DNS del servizio Docker
      # che ospita l'applicazione frontend.
      #
      # 8080 è la porta interna sulla quale il frontend
      # accetta le richieste HTTP.
      #
      # Il nome deve corrispondere al nome del servizio
      # presente nel file docker-compose.yml.
      - targets: ["frontend-products:8080"]


  # ----------------------------------------------------------
  # JOB 3: MONITORAGGIO DI PROMETHEUS
  # ----------------------------------------------------------

  # Prometheus espone metriche anche sul proprio funzionamento.
  #
  # Questo job consente quindi a Prometheus di monitorare
  # sé stesso, raccogliendo informazioni come:
  #
  # - utilizzo della CPU;
  # - memoria utilizzata;
  # - numero di serie temporali;
  # - durata delle query;
  # - richieste HTTP ricevute;
  # - stato del database TSDB.
  #
  # Le metriche avranno la label:
  #
  #   job="prometheus"
  - job_name: "prometheus"

    # Anche Prometheus viene dichiarato come target statico.
    static_configs:

      # localhost indica il container Prometheus stesso.
      #
      # Non indica il computer Windows, WSL o l'host Docker:
      # all'interno di un container, localhost identifica
      # il container corrente.
      #
      # La porta 9090 è la porta predefinita di Prometheus.
      #
      # Poiché metrics_path non è indicato esplicitamente,
      # Prometheus utilizza il valore predefinito:
      #
      #   /metrics
      #
      # URL completo:
      #
      #   http://localhost:9090/metrics
      - targets: ["localhost:9090"]
```

## Verifica rapida

Dopo aver avviato Prometheus, è possibile controllare lo stato dei target dall'interfaccia web:

```text
http://localhost:9090/targets
```

La query PromQL più semplice per verificare lo stato dei target è:

```promql
up
```

Interpretazione:

- `up = 1`: il target è raggiungibile e lo scraping è riuscito;
- `up = 0`: il target non è raggiungibile oppure l'endpoint `/metrics` non restituisce dati validi.
