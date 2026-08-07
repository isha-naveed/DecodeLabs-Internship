from app.services.ai_client import AIClient
from app.services.memory import ConversationMemory


class ChatService:
    """Coordinates conversation memory and AI responses."""

    def __init__(self):
        self.ai_client = AIClient()

    def send_message(
        self,
        message: str,
        memory: ConversationMemory,
    ) -> str:
        """
        Add the user message, generate an AI response,
        and store the assistant response.
        """

        memory.add_user_message(message)

        try:
            response = self.ai_client.get_response(
                memory.get_messages()
            )

            memory.add_assistant_message(response)

            return response

        except Exception:
            # Remove the user message if AI generation fails.
            memory.messages.pop()
            raise