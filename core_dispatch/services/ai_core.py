from openai import OpenAI
from ..config.settings import settings


class AICore:
    """
    Handles all interactions with the AI model via Ollama.
    """

    def __init__(self):
        """
        Initializes the AI core with a connection to the Ollama server.
        """
        self.client = OpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama",  # Required but not used by Ollama
        )
        self.model = settings.OLLAMA_MODEL

    def generate_text_response(self, prompt: str) -> str | None:
        """
        Generates a text-based response from the AI model.

        Args:
            prompt: The user's text prompt.

        Returns:
            The AI's text response, or None if an error occurs.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text response: {e}")
            return None

