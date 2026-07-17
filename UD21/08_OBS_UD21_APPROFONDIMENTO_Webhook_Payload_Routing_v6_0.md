# OBS UD21 — Approfondimento
# Webhook Grafana: payload, test, firing, resolved e routing

## 1. Che cosa fa un webhook

Un webhook è una chiamata HTTP avviata dal sistema che genera l'evento. In questo caso Grafana è il client e il receiver locale è il server.

```text
Grafana Alerting
   └─ HTTP POST application/json
          ↓
webhook-receiver:5001/grafana-alert
```

Il receiver risponde con uno status HTTP `2xx`. Grafana interpreta una risposta non riuscita come errore di consegna.

---

## 2. Payload semplificato

Un payload reale contiene più campi, ma la struttura essenziale è simile a questa:

```json
{
  "receiver": "UD21 - Webhook locale",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "UD21 - Products high error rate",
        "service": "products-frontend",
        "severity": "warning",
        "ud": "UD21"
      },
      "annotations": {
        "summary": "Error rate elevato sugli endpoint products",
        "description": "Verificare dashboard, log frontend/backend e trace Jaeger."
      }
    }
  ]
}
```

Il receiver salva l'intero documento ricevuto; la pagina web ne evidenzia i campi più utili.

---

## 3. Tre tipi di evento da riconoscere

### Test notification

Viene generata premendo `Test` nel contact point. Dimostra solo la raggiungibilità del canale.

### Firing

Viene generata quando la regola entra nello stato di allarme dopo il pending period.

### Resolved

Viene generata quando la condizione torna normale, se l'invio delle notifiche di risoluzione è abilitato.

La prova completa non termina con il test del contact point: deve includere almeno un `firing` e un `resolved` reali.

---

## 4. Contact point diretto e notification policy

### Percorso usato nel laboratorio

```text
Alert rule → Select contact point → UD21 - Webhook locale
```

È il percorso più trasparente per capire la relazione uno-a-uno.

### Percorso tipico in ambienti più grandi

```text
Alert rule con labels
       ↓
Notification policy tree
       ↓ matcher severity/service/team
Contact point appropriato
```

Esempio concettuale:

```text
severity=critical → reperibilità
severity=warning  → canale team
service=payments  → team pagamenti
```

Le label non servono soltanto a descrivere l'alert: possono governare il routing.

---

## 5. Test tecnico del receiver

Dal computer host:

```bash
curl -i http://localhost:5001/health
```

Test manuale di un payload:

```bash
curl -i \
  -H 'Content-Type: application/json' \
  -d '{"status":"manual-test","alerts":[]}' \
  http://localhost:5001/grafana-alert
```

Visualizzazione:

```text
http://localhost:5001/events
```

Questo test verifica il receiver, ma non verifica ancora la rete container-to-container di Grafana.

---

## 6. Test della rete Docker

Il test più significativo è quello eseguito dalla GUI del contact point Grafana, perché la richiesta parte realmente dal container Grafana verso:

```text
webhook-receiver:5001
```

Se fallisce:

```bash
docker compose ps
docker logs ud21-webhook-receiver --tail 100
docker logs ud21-grafana --tail 100
```

Controllo DNS/rete da un container Python presente su `obs-net`:

```bash
docker compose exec frontend-products python -c \
'import requests; print(requests.get("http://webhook-receiver:5001/health", timeout=3).json())'
```

---

## 7. Sicurezza

Il receiver della UD è intenzionalmente minimale e locale:

- non richiede autenticazione;
- non verifica firme HMAC;
- espone la pagina eventi;
- non deve essere pubblicato su Internet.

In produzione un webhook dovrebbe normalmente prevedere almeno una combinazione di:

- HTTPS;
- autenticazione o token;
- allowlist di rete;
- verifica della firma;
- rate limiting;
- gestione sicura dei segreti;
- retry e idempotenza.

La semplicità del laboratorio serve a rendere visibile il meccanismo, non rappresenta una configurazione pronta per Internet.

---

## 8. Pulizia degli eventi

Dalla pagina `/events` è disponibile il pulsante di cancellazione. In alternativa:

```bash
curl -X POST http://localhost:5001/clear
```

La cancellazione svuota il file nel volume `webhook-data`, ma non elimina il volume.
