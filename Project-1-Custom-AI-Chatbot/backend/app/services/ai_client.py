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

        system_message = {
            "role": "system",
            "content": (
                "You are a helpful AI assistant created by Isha Naveed. "
                "If the user asks who created, built, developed, or made you, "
                "clearly state that you were created by Isha Naveed. "
                "Do not claim to be created by OpenAI, Groq, Meta, or any other company or person."
            ),
        }

        conversation = [system_message] + messages

        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=conversation,
        )

        return response.choices[0].message.content
