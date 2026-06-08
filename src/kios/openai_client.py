from openai import OpenAI


class OpenAIClient:
    def __init__(self, model: str = "gpt-5-mini") -> None:
        self._client = OpenAI()
        self._model = model

    def generate_text(self, prompt: str) -> str:
        response = self._client.responses.create(
            model=self._model,
            input=prompt,
        )

        return response.output_text
