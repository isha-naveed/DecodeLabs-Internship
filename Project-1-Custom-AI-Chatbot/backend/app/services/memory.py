from app.prompts.prompts import SYSTEM_PROMPT

class ConversationMemory:
    """
    Manages the conversation history for the current chat session.
    Keeps the system prompt and the latest conversation turns.
    """

    MAX_TURNS: int = 2

    def __init__(self):
        self.system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }

        self.messages = [self.system_message]

    def add_user_message(self, message: str):
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str):
        self.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

        # Prune only after a complete turn (user + assistant)
        self._prune_history()

    def get_messages(self):
        return self.messages.copy()

    def clear(self):
        self.messages = [self.system_message]

    def get_history(self):
        return self.messages[1:].copy()

    def _prune_history(self):
        """
        Keeps only the latest MAX_TURNS conversation turns.
        One turn = User + Assistant.
        """

        conversation = self.messages[1:]

        max_messages = self.MAX_TURNS * 2

        if len(conversation) > max_messages:
            conversation = conversation[-max_messages:]

        self.messages = [self.system_message] + conversation