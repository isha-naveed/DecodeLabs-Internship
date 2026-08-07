from groq import Groq

from app.core.config import GROQ_API_KEY

class AIClient:
    """Handles communication with the Groq LLM API."""

    MODEL = "llama-3.3-70b-versatile"

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def get_response(self, messages: list[dict[str, str]]) -> str:
        """
        Send conversation messages to Groq and return the assistant response.
        """
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
        )

        return response.choices[0].message.content