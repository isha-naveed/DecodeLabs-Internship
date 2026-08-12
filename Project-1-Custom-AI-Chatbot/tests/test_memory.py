from app.services.memory import ConversationMemory


def test_memory_stores_conversation():
    memory = ConversationMemory()

    memory.add_user_message("Hello")
    memory.add_assistant_message("Hi there")

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there"


def test_memory_clear():
    memory = ConversationMemory()

    memory.add_user_message("Hello")
    memory.add_assistant_message("Hi")

    memory.clear()

    assert memory.get_history() == []
    assert len(memory.get_messages()) == 1
    assert memory.get_messages()[0]["role"] == "system"


def test_memory_prunes_old_turns():
    memory = ConversationMemory()

    for i in range(3):
        memory.add_user_message(f"user {i}")
        memory.add_assistant_message(f"assistant {i}")

    history = memory.get_history()

    assert len(history) == 4
    assert history[0]["content"] == "user 1"
    assert history[-1]["content"] == "assistant 2"
