# Runbook minimo — Catalogo prodotti

## Sintomo: `/products` non risponde

1. Verificare `/health` frontend.
2. Verificare `/ready` frontend.
3. Verificare backend health.
4. Controllare AppRequests.
5. Controllare ContainerAppConsoleLogs_CL.
6. Controllare revisioni ACA.

## Sintomo: `/products/slow` lento

1. Misurare latenza curl.
2. Controllare Grafana p95.
3. Controllare Jaeger span backend.
4. Controllare AppDependencies DurationMs.
5. Verificare se il problema è localizzato o generale.

## Sintomo: `/products/error` 500

1. Verificare AppRequests ResultCode 500.
2. Verificare AppExceptions.
3. Cercare request_id nei log.
4. Distinguere errore applicativo da revisione unhealthy.
5. Valutare rollback o correzione codice.
