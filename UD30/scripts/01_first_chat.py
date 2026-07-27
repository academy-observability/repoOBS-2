"""Prima chiamata a un modello locale tramite il client Python Ollama."""

from __future__ import annotations

try:
    from ollama import Client
except ImportError:
    print("Package 'ollama' non installato. Usa: pip install -r requirements.txt")
    raise SystemExit(2)

from common import call_chat, get_host, get_model_name

PROMPT = (
    "Spiega in poche righe la differenza tra un fatto osservato "
    "e un'ipotesi diagnostica in un incidente applicativo."
)


def main() -> None:
    model = get_model_name()
    client = Client(host=get_host())
    result = call_chat(client, model, PROMPT)

    print("=== CONFIGURAZIONE ===")
    print(f"Modello richiesto: {model}")
    print(f"Status: {result.status}")

    if result.status != "success":
        print(f"Errore: {result.error}")
        raise SystemExit(1)

    print("\n=== RISPOSTA DEL MODELLO ===")
    print(result.content.strip())

    print("\n=== METADATI ===")
    print(f"Modello effettivo: {result.model}")
    print(f"Latenza osservata dal client: {result.client_latency_ms:.2f} ms")
    print(f"Durata totale Ollama: {result.ollama_total_ms:.2f} ms")
    print(f"Caricamento modello: {result.load_ms:.2f} ms")
    print(f"Valutazione prompt: {result.prompt_eval_ms:.2f} ms")
    print(f"Generazione: {result.generation_ms:.2f} ms")
    print(f"Token prompt: {result.prompt_tokens}")
    print(f"Token generati: {result.output_tokens}")


if __name__ == "__main__":
    main()
