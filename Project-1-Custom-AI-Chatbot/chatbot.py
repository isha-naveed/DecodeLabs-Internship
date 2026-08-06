from ai_client import get_ai_response
from memory import ConversationMemory
from commands import handle_command
memory = ConversationMemory()

print("======================================")
print("      AI Chatbot with Memory")
print("======================================")
print("Type '/help' to see available commands.\n")

while True:

    user_input = input("You: ").strip()

    if not user_input:
        continue

    # Exit
    command_result = handle_command(user_input, memory)

    if command_result is False:
        break
    
    if command_result is True:
        continue

    # Save user message
    memory.add_user_message(user_input)

    try:

        bot_reply = get_ai_response(memory.get_messages())

        print(f"\nBot: {bot_reply}\n")

        # Save assistant reply
        memory.add_assistant_message(bot_reply)

    except Exception as e:
        print(f"\n❌ Error: {e}\n")