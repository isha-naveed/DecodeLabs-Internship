from app.services.memory import ConversationMemory


def test_memory_starts_with_system_message():
    memory = ConversationMemory()

    messages = memory.get_messages()

    assert len(messages) == 1
    assert messages[0]["role"] == "system"


def test_memory_stores_conversation():
    memory = ConversationMemory()

    memory.add_user_message("My name is Isha.")
    memory.add_assistant_message("Nice to meet you, Isha.")

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["content"] == "My name is Isha."
    assert history[1]["content"] == "Nice to meet you, Isha."


def test_memory_clear():
    memory = ConversationMemory()

    memory.add_user_message("Hello")
    memory.add_assistant_message("Hi!")

    memory.clear()

    assert memory.get_history() == []
    assert len(memory.get_messages()) == 1
    assert memory.get_messages()[0]["role"] == "system"


def test_memory_prunes_old_turns():
    memory = ConversationMemory()

    for i in range(3):
        memory.add_user_message(f"User {i}")
        memory.add_assistant_message(f"Assistant {i}")

    history = memory.get_history()

    assert len(history) == 4
    assert history[0]["content"] == "User 1"
    assert history[-1]["content"] == "Assistant 2"