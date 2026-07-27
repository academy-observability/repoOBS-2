"""Funzioni comuni per gli script della UD30.

Il file contiene solo codice di servizio: lettura file, conversione delle durate
Ollama e normalizzazione della risposta. I laboratori spiegano quali parti devono
essere comprese e quali possono essere considerate infrastruttura di supporto.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "llama3.2:1b"
DEFAULT_HOST = "http://localhost:11434"


def get_model_name() -> str:
    """Restituisce il modello configurato o il modello di riferimento."""
    return os.getenv("OLLAMA_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def get_host() -> str:
    """Restituisce l'host del servizio Ollama."""
    return os.getenv("OLLAMA_HOST", DEFAULT_HOST).strip() or DEFAULT_HOST


def read_text(relative_path: str) -> str:
    path = BASE_DIR / relative_path
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {path}")
    return path.read_text(encoding="utf-8")


def build_prompt(template_relative_path: str, evidence_relative_path: str) -> str:
    template = read_text(template_relative_path)
    evidence = read_text(evidence_relative_path)
    placeholder = "{{EVIDENCE_PACKET}}"
    if placeholder not in template:
        raise ValueError(f"Segnaposto {placeholder} non presente nel template")
    return template.replace(placeholder, evidence)


def value_from(obj: Any, name: str, default: Any = None) -> Any:
    """Legge un campo sia da oggetti tipizzati sia da dizionari."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def nested_value(obj: Any, parent: str, child: str, default: Any = None) -> Any:
    return value_from(value_from(obj, parent), child, default)


def ns_to_ms(value: Any) -> float:
    """Converte i nanosecondi restituiti da Ollama in millisecondi."""
    try:
        return round(float(value or 0) / 1_000_000, 2)
    except (TypeError, ValueError):
        return 0.0


@dataclass
class CallResult:
    model: str
    status: str
    content: str
    client_latency_ms: float
    ollama_total_ms: float
    load_ms: float
    prompt_eval_ms: float
    generation_ms: float
    prompt_tokens: int
    output_tokens: int
    error: str = ""

    @property
    def response_length(self) -> int:
        return len(self.content)


def call_chat(client: Any, model: str, prompt: str) -> CallResult:
    """Esegue una chiamata non streaming e normalizza i metadati principali."""
    started = time.perf_counter()
    try:
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            options={"temperature": 0.2},
        )
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return CallResult(
            model=str(value_from(response, "model", model)),
            status="success",
            content=str(nested_value(response, "message", "content", "")),
            client_latency_ms=latency_ms,
            ollama_total_ms=ns_to_ms(value_from(response, "total_duration", 0)),
            load_ms=ns_to_ms(value_from(response, "load_duration", 0)),
            prompt_eval_ms=ns_to_ms(value_from(response, "prompt_eval_duration", 0)),
            generation_ms=ns_to_ms(value_from(response, "eval_duration", 0)),
            prompt_tokens=int(value_from(response, "prompt_eval_count", 0) or 0),
            output_tokens=int(value_from(response, "eval_count", 0) or 0),
        )
    except Exception as exc:  # il tipo concreto dipende dal client e dalla rete
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return CallResult(
            model=model,
            status="error",
            content="",
            client_latency_ms=latency_ms,
            ollama_total_ms=0.0,
            load_ms=0.0,
            prompt_eval_ms=0.0,
            generation_ms=0.0,
            prompt_tokens=0,
            output_tokens=0,
            error=str(exc),
        )
