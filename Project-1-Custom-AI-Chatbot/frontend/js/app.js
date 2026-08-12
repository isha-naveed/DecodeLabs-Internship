const API_BASE = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");
const username = localStorage.getItem("username");

if (!token) {
    window.location.href = "login.html";
}

const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const status = document.getElementById("status");
const sendBtn = document.getElementById("sendBtn");

const newChatBtn = document.getElementById("newChatBtn");
const clearBtn = document.getElementById("headerClearBtn");
const logoutBtn = document.getElementById("logoutBtn");
const userAvatar = document.getElementById("userAvatar");


/* =========================
   USERNAME
========================= */

if (usernameDisplay && username) {
    usernameDisplay.textContent = username;
}

if (userAvatar && username) {
    userAvatar.textContent = username.charAt(0).toUpperCase();
}


/* =========================
   ADD MESSAGE
========================= */

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


/* =========================
   RESET CHAT UI
========================= */

function resetChatUI(message = "New conversation started. How can I help you?") {
    messages.innerHTML = "";

    addMessage(message, "assistant");

    status.textContent = "";
    messageInput.value = "";
    messageInput.focus();
}


/* =========================
   SEND MESSAGE
========================= */

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
            localStorage.removeItem("username");
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


/* =========================
   NEW CHAT
========================= */

newChatBtn.addEventListener("click", async () => {
    try {
        const response = await fetch(`${API_BASE}/chat/clear`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("username");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            throw new Error("Unable to start new chat.");
        }

        resetChatUI();

    } catch (error) {
        status.textContent = "Unable to start new chat.";
        console.error(error);
    }
});


/* =========================
   CLEAR CHAT
========================= */

clearBtn.addEventListener("click", async () => {
    try {
        const response = await fetch(`${API_BASE}/chat/clear`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("username");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            throw new Error("Unable to clear conversation.");
        }

        resetChatUI(
            "Conversation cleared. What would you like to talk about?"
        );

    } catch (error) {
        status.textContent = "Unable to clear conversation.";
        console.error(error);
    }
});


/* =========================
   LOGOUT
========================= */

logoutBtn.addEventListener("click", async () => {
    try {
        await fetch(`${API_BASE}/chat/clear`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

    } catch (error) {
        console.error(
            "Unable to clear conversation during logout.",
            error
        );

    } finally {
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");

        window.location.href = "login.html";
    }
});