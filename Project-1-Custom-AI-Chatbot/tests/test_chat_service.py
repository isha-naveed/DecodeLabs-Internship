from app.services.chat_service import ChatService
from app.services.memory import ConversationMemory


def test_chat_service_stores_user_and_assistant_messages(monkeypatch):
    service = ChatService()
    memory = ConversationMemory()

    def fake_get_response(messages):
        return "Test response"

    monkeypatch.setattr(
        service.ai_client,
        "get_response",
        fake_get_response,
    )

    response = service.send_message("Hello", memory)

    assert response == "Test response"

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Test response"


def test_chat_service_removes_user_message_when_ai_fails(monkeypatch):
    service = ChatService()
    memory = ConversationMemory()

    def fake_get_response(messages):
        raise RuntimeError("AI service failed")

    monkeypatch.setattr(
        service.ai_client,
        "get_response",
        fake_get_response,
    )

    try:
        service.send_message("Hello", memory)
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass

    assert memory.get_history() == []
