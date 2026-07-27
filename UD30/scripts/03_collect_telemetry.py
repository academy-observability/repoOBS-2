"""Esegue più chiamate Ollama e registra telemetria in CSV."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

try:
    from ollama import Client
except ImportError:
    print("Package 'ollama' non installato. Usa: pip install -r requirements.txt")
    raise SystemExit(2)

from common import BASE_DIR, build_prompt, call_chat, get_host, get_model_name

CSV_PATH = BASE_DIR / "runtime" / "ollama_runs.csv"
RESPONSES_DIR = BASE_DIR / "runtime" / "telemetry_responses"
FIELDNAMES = [
    "timestamp",
    "run_id",
    "model",
    "prompt_type",
    "status",
    "client_latency_ms",
    "ollama_total_ms",
    "load_ms",
    "prompt_eval_ms",
    "generation_ms",
    "prompt_tokens",
    "output_tokens",
    "response_length",
    "response_file",
    "error",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3, help="Numero di cicli")
    parser.add_argument("--append", action="store_true", help="Non sovrascrivere il CSV")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.runs < 1 or args.runs > 20:
        raise SystemExit("--runs deve essere compreso tra 1 e 20")

    model = get_model_name()
    client = Client(host=get_host())
    prompts = {
        "open": build_prompt("prompts/prompt_aperto.txt", "evidence/incident_catalogo_guidato.md"),
        "constrained": build_prompt("prompts/prompt_vincolato.txt", "evidence/incident_catalogo_guidato.md"),
    }

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.append and CSV_PATH.exists() else "w"

    with CSV_PATH.open(mode, newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        if mode == "w":
            writer.writeheader()

        for cycle in range(1, args.runs + 1):
            for prompt_type, prompt in prompts.items():
                run_id = f"run-{cycle:02d}-{prompt_type}"
                print(f"Esecuzione {run_id} con {model}...")
                result = call_chat(client, model, prompt)
                response_file = ""
                if result.status == "success":
                    path = RESPONSES_DIR / f"{run_id}_{model.replace(':', '_')}.md"
                    path.write_text(result.content.strip() + "\n", encoding="utf-8")
                    response_file = str(path.relative_to(BASE_DIR))

                writer.writerow(
                    {
                        "timestamp": datetime.now().isoformat(timespec="seconds"),
                        "run_id": run_id,
                        "model": result.model,
                        "prompt_type": prompt_type,
                        "status": result.status,
                        "client_latency_ms": result.client_latency_ms,
                        "ollama_total_ms": result.ollama_total_ms,
                        "load_ms": result.load_ms,
                        "prompt_eval_ms": result.prompt_eval_ms,
                        "generation_ms": result.generation_ms,
                        "prompt_tokens": result.prompt_tokens,
                        "output_tokens": result.output_tokens,
                        "response_length": result.response_length,
                        "response_file": response_file,
                        "error": result.error,
                    }
                )
                handle.flush()

    print(f"Telemetria salvata in: {CSV_PATH}")


if __name__ == "__main__":
    main()
