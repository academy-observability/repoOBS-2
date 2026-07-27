"""Confronta prompt aperto e prompt vincolato sullo stesso evidence packet."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    from ollama import Client
except ImportError:
    print("Package 'ollama' non installato. Usa: pip install -r requirements.txt")
    raise SystemExit(2)

from common import BASE_DIR, build_prompt, call_chat, get_host, get_model_name

OUTPUT_DIR = BASE_DIR / "runtime" / "responses"


def save_response(label: str, content: str, model: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{label}_{model.replace(':', '_')}.md"
    path.write_text(
        f"# Risposta {label}\n\n"
        f"- Modello: `{model}`\n"
        f"- Data: `{datetime.now().isoformat(timespec='seconds')}`\n\n"
        f"{content.strip()}\n",
        encoding="utf-8",
    )
    return path


def run_one(client: Client, model: str, label: str, prompt: str) -> None:
    print(f"\n=== {label.upper()} ===")
    result = call_chat(client, model, prompt)
    if result.status != "success":
        print(f"Errore: {result.error}")
        return

    path = save_response(label, result.content, result.model)
    print(result.content.strip())
    print("\nMetadati:")
    print(f"  modello: {result.model}")
    print(f"  latenza client: {result.client_latency_ms:.2f} ms")
    print(f"  token prompt: {result.prompt_tokens}")
    print(f"  token output: {result.output_tokens}")
    print(f"  file: {path}")


def main() -> None:
    model = get_model_name()
    client = Client(host=get_host())
    open_prompt = build_prompt(
        "prompts/prompt_aperto.txt",
        "evidence/incident_catalogo_guidato.md",
    )
    constrained_prompt = build_prompt(
        "prompts/prompt_vincolato.txt",
        "evidence/incident_catalogo_guidato.md",
    )

    print(f"Modello: {model}")
    run_one(client, model, "prompt_aperto", open_prompt)
    run_one(client, model, "prompt_vincolato", constrained_prompt)


if __name__ == "__main__":
    main()
