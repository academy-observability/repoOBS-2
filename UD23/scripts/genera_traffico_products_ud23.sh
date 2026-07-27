#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8080}"

echo "Generazione traffico verso ${BASE_URL}"
for i in {1..10}; do curl -s "${BASE_URL}/products" > /dev/null || true; done
for i in {1..4};  do curl -s "${BASE_URL}/products/slow" > /dev/null || true; done
for i in {1..4};  do curl -s "${BASE_URL}/products/error" > /dev/null || true; done

echo "Traffico completato."
