from utils import show_help, show_history


def handle_command(command: str, memory):
    """
    Handles chatbot commands.

    Returns:
        True  -> Continue chatbot
        False -> Exit chatbot
        None  -> Not a command
    """

    command = command.lower()

    if command in ["/exit", "exit"]:
        print("\nBot: Goodbye!")
        return False

    if command == "/help":
        show_help()
        return True

    if command == "/history":
        show_history(memory.get_history())
        return True

    if command == "/clear":
        memory.clear()
        print("\n✅ Conversation memory cleared.\n")
        return True

    return None