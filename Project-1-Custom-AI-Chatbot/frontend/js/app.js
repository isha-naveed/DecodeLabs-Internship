const API_BASE = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "login.html";
}

const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const status = document.getElementById("status");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const logoutBtn = document.getElementById("logoutBtn");

function addMessage(text, role) {
    const message = document.createElement("div");
    message.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    message.appendChild(bubble);
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";
    sendBtn.disabled = true;
    status.textContent = "AI is thinking...";

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                message: message
            })
        });

        if (response.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            throw new Error("Chat request failed.");
        }

        const data = await response.json();

        addMessage(data.response, "assistant");

    } catch (error) {
        addMessage(
            "Sorry, something went wrong. Please try again.",
            "assistant"
        );
        console.error(error);

    } finally {
        sendBtn.disabled = false;
        status.textContent = "";
        messageInput.focus();
    }
});

clearBtn.addEventListener("click", async () => {
    try {
        const response = await fetch(`${API_BASE}/chat/clear`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Unable to clear conversation.");
        }

        messages.innerHTML = "";

        addMessage(
            "Conversation cleared. What would you like to talk about?",
            "assistant"
        );

    } catch (error) {
        status.textContent = "Unable to clear conversation.";
        console.error(error);
    }
});

logoutBtn.addEventListener("click", async () => {
    try {
        await fetch(`${API_BASE}/chat/clear`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
    } catch (error) {
        console.error("Unable to clear conversation during logout.", error);
    } finally {
        localStorage.removeItem("access_token");
        window.location.href = "login.html";
    }
});
