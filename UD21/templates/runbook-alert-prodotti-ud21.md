# UD21 — Runbook alert Catalogo prodotti

## Alert: ProductsHighErrorRate

### Sintomo

L'error rate user-facing del frontend sugli endpoint `/products*` è superiore alla soglia per il pending period configurato.

### Prime verifiche

1. Aprire la alert rule e leggere valore A e stato B.
2. Aprire la dashboard UD21.
3. Eseguire la query di scomposizione per servizio, path e status.
4. Verificare log frontend e backend:

```bash
docker logs ud21-products-frontend --tail 120
docker logs ud21-products-backend --tail 120
```

5. Individuare eventuali `request_id` e `trace_id`.
6. Aprire Jaeger e cercare trace fallite.

### Ipotesi

- chiamate controllate a `/products/error`;
- errore originato dal backend e propagato dal frontend;
- backend non raggiungibile;
- timeout frontend → backend;
- filtro PromQL errato;
- traffico di test non rappresentativo.

### Verifica della notifica

Aprire:

```text
http://localhost:5001/events
```

Controllare:

- `status=firing`;
- labels `service`, `severity`, `ud`, `signal`;
- summary e description;
- successivo `status=resolved`.

### Chiusura

Documentare causa, evidenza decisiva, azione e momento del rientro.

---

## Alert: ProductsHighLatencyP95

### Sintomo

La latenza p95 user-facing degli endpoint `/products*` supera 1,5 secondi.

### Prime verifiche

1. Confrontare p95 e request rate.
2. Verificare la presenza di `/products/slow`.
3. Aprire Jaeger e individuare trace lente.
4. Confrontare durata span frontend e backend.
5. Controllare log e timeout.

### Chiusura

Documentare se il ritardo è nel frontend, nel backend o nella dipendenza.

---

## Persistenza e continuità operativa

Se la regola o gli eventi sembrano scomparsi:

```bash
./scripts/inspect_volumes_ud21.sh
```

Verificare di non aver eseguito un reset con eliminazione dei volumi.
