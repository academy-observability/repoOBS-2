from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from common import call_chat, ns_to_ms


class Message:
    content = "Risposta di test"


class Response:
    model = "fake:1b"
    message = Message()
    total_duration = 2_000_000
    load_duration = 500_000
    prompt_eval_duration = 600_000
    eval_duration = 900_000
    prompt_eval_count = 12
    eval_count = 7


class FakeClient:
    def chat(self, **kwargs):
        return Response()


def test_ns_to_ms():
    assert ns_to_ms(2_500_000) == 2.5


def test_call_chat_success():
    result = call_chat(FakeClient(), "fake:1b", "prompt")
    assert result.status == "success"
    assert result.content == "Risposta di test"
    assert result.ollama_total_ms == 2.0
    assert result.prompt_tokens == 12
    assert result.output_tokens == 7
