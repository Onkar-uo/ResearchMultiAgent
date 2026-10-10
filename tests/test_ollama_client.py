from pydantic import BaseModel, ConfigDict, Field

from app.llm.ollama_client import OllamaClient, OllamaError


class SmallResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(min_length=1)


def test_structured_output_retries_malformed_json(monkeypatch):
    client = OllamaClient()
    responses = iter(["not json", '{"summary": "validated"}'])

    def fake_generate(_prompt, _system_prompt=None):
        return next(responses)

    monkeypatch.setattr(client, "generate", fake_generate)

    result = client.generate_structured("Return a summary", SmallResult)

    assert result.summary == "validated"


def test_structured_output_raises_after_invalid_schema(monkeypatch):
    client = OllamaClient()

    def fake_generate(_prompt, _system_prompt=None):
        return '{"unexpected": true}'

    monkeypatch.setattr(client, "generate", fake_generate)

    try:
        client.generate_structured("Return a summary", SmallResult)
    except OllamaError as exc:
        assert "validation" in str(exc)
    else:
        raise AssertionError("Invalid structured output should be rejected.")
