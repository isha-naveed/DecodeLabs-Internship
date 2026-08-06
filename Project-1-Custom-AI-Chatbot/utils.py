def show_help():
    print("\nAvailable Commands:")
    print("  /help     - Show available commands")
    print("  /history  - Show current conversation")
    print("  /clear    - Clear conversation memory")
    print("  /exit      - Exit chatbot\n")


def show_history(messages):
    print("\n========== Conversation History ==========")

    for message in messages:
        role = message["role"]

        if role == "system":
            continue

        if role == "user":
            print(f"You : {message['content']}")
        else:
            print(f"Bot : {message['content']}")

    print("==========================================\n")