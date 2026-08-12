const API_BASE = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const status = document.getElementById("status");

function showStatus(message, isError = false) {
    status.textContent = message;
    status.style.color = isError ? "#dc2626" : "#16a34a";
}

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;

        try {
            showStatus("Logging in...");

            const response = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Login failed.");
            }

            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("username", username);
            window.location.href = "index.html";

        } catch (error) {
            showStatus(error.message, true);
        }
    });
}

if (signupForm) {
    signupForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        try {
            showStatus("Creating account...");

            const response = await fetch(`${API_BASE}/auth/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Signup failed.");
            }

            showStatus("Account created. Redirecting to login...");

            setTimeout(() => {
                window.location.href = "login.html";
            }, 800);

        } catch (error) {
            showStatus(error.message, true);
        }
    });
}
