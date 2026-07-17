# OBS UD21 — Approfondimento
# Volumi Docker e persistenza dello stack di alerting

## 1. Il problema che risolviamo

Un container è sostituibile. Quando viene eliminato, il suo filesystem scrivibile non deve essere considerato un archivio affidabile.

Nella UD21 creiamo oggetti importanti dalla GUI:

- contact point webhook;
- alert rule;
- folder;
- evaluation group;
- cronologia degli stati.

Se `/var/lib/grafana` non è montato su un volume, una ricreazione del container può eliminare questi oggetti.

---

## 2. I mount presenti nel compose

Estratto semplificato:

```yaml
services:
  prometheus:
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus

  grafana:
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro

  webhook-receiver:
    volumes:
      - webhook-data:/data

volumes:
  grafana-data:
    name: obs-ud21-grafana-data
  prometheus-data:
    name: obs-ud21-prometheus-data
  webhook-data:
    name: obs-ud21-webhook-data
```

---

## 3. Configurazione e dati runtime

La distinzione essenziale è:

```text
file nel repository → bind mount
stato prodotto dai servizi → named volume
```

| Contenuto | Meccanismo | Motivo |
|---|---|---|
| `prometheus.yml` | bind mount read-only | deve essere versionato |
| provisioning Grafana | bind mount read-only | configurazione riproducibile |
| dashboard JSON | bind mount read-only | dashboard as code |
| database Grafana | named volume | contiene stato runtime |
| TSDB Prometheus | named volume | contiene campioni metrici |
| eventi webhook | named volume | contiene notifiche ricevute |

---

## 4. Verifica dei volumi

```bash
./scripts/inspect_volumes_ud21.sh
```

Oppure manualmente:

```bash
docker volume ls --filter name=obs-ud21
```

Dettagli:

```bash
docker volume inspect obs-ud21-grafana-data
docker volume inspect obs-ud21-prometheus-data
docker volume inspect obs-ud21-webhook-data
```

Verifica dei mount dichiarati sui container:

```bash
docker inspect ud21-grafana \
  --format '{{range .Mounts}}{{println .Type .Name .Destination}}{{end}}'
```

```bash
docker inspect ud21-prometheus \
  --format '{{range .Mounts}}{{println .Type .Name .Destination}}{{end}}'
```

```bash
docker inspect ud21-webhook-receiver \
  --format '{{range .Mounts}}{{println .Type .Name .Destination}}{{end}}'
```

---

## 5. Prova di persistenza guidata

Dopo aver creato il contact point e la regola:

```bash
./scripts/stop_stack_ud21.sh
./scripts/start_stack_ud21.sh
```

Verificare:

1. il contact point `UD21 - Webhook locale` esiste ancora;
2. la regola `UD21 - Products high error rate` esiste ancora;
3. gli eventi precedenti sono ancora visibili su `/events`;
4. Prometheus conserva la cronologia precedente.

Questa prova dimostra la persistenza meglio di una definizione teorica.

---

## 6. Reset controllato

Per ricominciare da zero:

```bash
RESET_UD21=yes ./scripts/reset_stack_ud21.sh
```

Lo script esegue una rimozione equivalente a:

```bash
docker compose down -v --remove-orphans
```

Dopo il reset:

- il contact point deve essere ricreato;
- le alert rule create dalla GUI non esistono più;
- la TSDB Prometheus riparte vuota;
- la pagina eventi del webhook riparte vuota.

---

## 7. Errori frequenti

### Usare sempre `down -v`

È un errore quando si vuole solo spegnere il laboratorio. `-v` significa cancellazione dei volumi associati al progetto.

### Confondere dashboard provisioned e regola GUI

La dashboard torna perché è presente nel repository e montata come file. La regola torna perché il database Grafana è nel volume. Sono due meccanismi diversi.

### Modificare direttamente il contenuto del volume

I named volume devono essere gestiti dai servizi. Non è buona pratica aprirli e modificare manualmente i file interni.

### Pensare che ogni servizio sia persistente

Nella UD21 Jaeger resta in memoria. Il fatto che Grafana e Prometheus siano persistenti non implica che lo siano tutti i componenti.

---

## 8. Regola operativa da ricordare

```text
stop/down senza -v → fermo e posso riprendere
reset/down -v       → cancello lo stato e ricomincio
```
