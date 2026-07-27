"""Codice di servizio condiviso dagli script UD30.

Centralizza:
- endpoint Ollama Windows raggiunto da WSL;
- modello di default;
- creazione del client;
- normalizzazione della risposta;
- conversione nanosecondi -> millisecondi.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llama3.2:1b"


def base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def model_name() -> str:
    return os.getenv("OLLAMA_MODEL", DEFAULT_MODEL).strip()


def build_client() -> Any:
    try:
        from ollama import Client
    except ImportError as exc:
        raise RuntimeError(
            "Package Python 'ollama' non disponibile. "
            "Attivare la .venv e installare requirements.txt."
        ) from exc
    return Client(host=base_url())


def field(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def ns_to_ms(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return round(float(value) / 1_000_000, 3)
    except (TypeError, ValueError):
        return None


def extract_model_names(list_response: Any) -> list[str]:
    models = field(list_response, "models", []) or []
    names: list[str] = []
    for item in models:
        name = field(item, "model") or field(item, "name")
        if name:
            names.append(str(name))
    return names


@dataclass
class ChatResult:
    timestamp: str
    model: str
    prompt_name: str
    success: bool
    client_duration_ms: float
    text: str = ""
    total_duration_ms: float | None = None
    load_duration_ms: float | None = None
    prompt_eval_count: int | None = None
    eval_count: int | None = None
    prompt_eval_duration_ms: float | None = None
    eval_duration_ms: float | None = None
    done_reason: str | None = None
    error: str = ""

    def row(self) -> dict[str, Any]:
        return asdict(self)


def chat(
    prompt: str,
    *,
    prompt_name: str,
    model: str | None = None,
    client: Any | None = None,
) -> ChatResult:
    selected_model = model or model_name()
    active_client = client or build_client()
    started = time.perf_counter()
    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    try:
        response = active_client.chat(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1},
        )
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        message = field(response, "message", {})
        text = field(message, "content", "") or ""
        return ChatResult(
            timestamp=timestamp,
            model=str(field(response, "model", selected_model)),
            prompt_name=prompt_name,
            success=True,
            client_duration_ms=elapsed,
            text=str(text),
            total_duration_ms=ns_to_ms(field(response, "total_duration")),
            load_duration_ms=ns_to_ms(field(response, "load_duration")),
            prompt_eval_count=field(response, "prompt_eval_count"),
            eval_count=field(response, "eval_count"),
            prompt_eval_duration_ms=ns_to_ms(field(response, "prompt_eval_duration")),
            eval_duration_ms=ns_to_ms(field(response, "eval_duration")),
            done_reason=field(response, "done_reason"),
        )
    except Exception as exc:  # errore riportato come dato osservabile
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        return ChatResult(
            timestamp=timestamp,
            model=selected_model,
            prompt_name=prompt_name,
            success=False,
            client_duration_ms=elapsed,
            error=f"{type(exc).__name__}: {exc}",
        )


def read_text(relative_path: str) -> str:
    root = Path(__file__).resolve().parent.parent
    return (root / relative_path).read_text(encoding="utf-8")


def fill_prompt(template_path: str, evidence_path: str) -> str:
    template = read_text(template_path)
    evidence = read_text(evidence_path)
    return template.replace("[INCOLLARE QUI]", evidence)
