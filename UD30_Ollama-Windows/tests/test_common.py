import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from common import chat, extract_model_names  # noqa: E402


class FakeMessage:
    content = "risposta di prova"


class FakeResponse:
    model = "fake:1b"
    message = FakeMessage()
    total_duration = 2_000_000_000
    load_duration = 500_000_000
    prompt_eval_count = 10
    eval_count = 20
    prompt_eval_duration = 200_000_000
    eval_duration = 1_000_000_000
    done_reason = "stop"


class FakeClient:
    def chat(self, **kwargs):
        return FakeResponse()


class CommonTests(unittest.TestCase):
    def test_extract_models(self):
        response = {"models": [{"model": "a:1b"}, {"name": "b:1b"}]}
        self.assertEqual(extract_model_names(response), ["a:1b", "b:1b"])

    def test_chat_normalization(self):
        result = chat(
            "prompt",
            prompt_name="test",
            model="fake:1b",
            client=FakeClient(),
        )
        self.assertTrue(result.success)
        self.assertEqual(result.text, "risposta di prova")
        self.assertEqual(result.total_duration_ms, 2000.0)
        self.assertEqual(result.eval_count, 20)


if __name__ == "__main__":
    unittest.main()
