"""Verifica preliminare dell'ambiente Ollama e Python."""

from __future__ import annotations

import sys

try:
    from ollama import Client
except ImportError:
    print("[ERRORE] Package Python 'ollama' non installato.")
    print("Attiva .venv e usa: pip install -r requirements.txt")
    raise SystemExit(2)

from common import call_chat, get_host, get_model_name, value_from


def main() -> int:
    model = get_model_name()
    host = get_host()
    print("[OK] package Python ollama disponibile")
    print(f"Host configurato: {host}")
    print(f"Modello configurato: {model}")

    client = Client(host=host)

    try:
        listed = client.list()
    except Exception as exc:
        print(f"[ERRORE] servizio Ollama non raggiungibile: {exc}")
        print("Avvia Ollama con 'ollama serve' o tramite il servizio di sistema.")
        return 3

    print("[OK] servizio Ollama raggiungibile")
    models = value_from(listed, "models", []) or []
    names = []
    for item in models:
        name = value_from(item, "model", value_from(item, "name", ""))
        if name:
            names.append(str(name))

    if names:
        print("Modelli locali:")
        for name in names:
            print(f"  - {name}")
    else:
        print("[ATTENZIONE] nessun modello locale rilevato")

    if model not in names:
        print(f"[ATTENZIONE] modello '{model}' non presente nell'elenco.")
        print(f"Scaricalo con: ollama pull {model}")
        return 4

    print("[OK] modello configurato disponibile")
    result = call_chat(
        client,
        model,
        "Rispondi con una sola frase: che cosa significa osservabilità?",
    )

    if result.status != "success":
        print(f"[ERRORE] richiesta non completata: {result.error}")
        return 5

    print("[OK] richiesta completata")
    print(f"Latenza client: {result.client_latency_ms:.2f} ms")
    print(f"Token output: {result.output_tokens}")
    print(f"Risposta: {result.content.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
