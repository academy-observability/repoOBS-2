"""Esegue lo stesso prompt vincolato con più modelli configurati."""

from __future__ import annotations

import csv
import os
from datetime import datetime

try:
    from ollama import Client
except ImportError:
    print("Package 'ollama' non installato. Usa: pip install -r requirements.txt")
    raise SystemExit(2)

from common import BASE_DIR, build_prompt, call_chat, get_host

OUTPUT = BASE_DIR / "runtime" / "model_comparison.csv"
RESPONSES = BASE_DIR / "runtime" / "model_comparison_responses"
FIELDS = [
    "timestamp",
    "model_requested",
    "model_effective",
    "status",
    "client_latency_ms",
    "ollama_total_ms",
    "load_ms",
    "prompt_tokens",
    "output_tokens",
    "response_length",
    "response_file",
    "error",
]


def configured_models() -> list[str]:
    raw = os.getenv("OLLAMA_MODELS", "llama3.2:1b,llama3.2:3b")
    models = [item.strip() for item in raw.split(",") if item.strip()]
    if len(models) < 2:
        raise SystemExit("Configurare almeno due modelli in OLLAMA_MODELS")
    return models


def main() -> None:
    models = configured_models()
    client = Client(host=get_host())
    prompt = build_prompt(
        "prompts/prompt_vincolato.txt",
        "evidence/incident_catalogo_guidato.md",
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    RESPONSES.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()

        for model in models:
            print(f"Esecuzione con {model}...")
            result = call_chat(client, model, prompt)
            response_file = ""
            if result.status == "success":
                path = RESPONSES / f"{model.replace(':', '_')}.md"
                path.write_text(result.content.strip() + "\n", encoding="utf-8")
                response_file = str(path.relative_to(BASE_DIR))

            writer.writerow(
                {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "model_requested": model,
                    "model_effective": result.model,
                    "status": result.status,
                    "client_latency_ms": result.client_latency_ms,
                    "ollama_total_ms": result.ollama_total_ms,
                    "load_ms": result.load_ms,
                    "prompt_tokens": result.prompt_tokens,
                    "output_tokens": result.output_tokens,
                    "response_length": result.response_length,
                    "response_file": response_file,
                    "error": result.error,
                }
            )

    print(f"Confronto salvato in: {OUTPUT}")
    print(f"Risposte salvate in: {RESPONSES}")


if __name__ == "__main__":
    main()
