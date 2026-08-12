# Custom AI Chatbot with Memory

A conversational AI chatbot built with FastAPI, JWT authentication, SQLAlchemy, Groq LLM, and session-based conversation memory.

## Features

- User signup and login
- JWT authentication
- Secure password hashing
- Groq LLM integration
- Llama 3.3 70B model
- Session-based conversation memory
- Conversation history pruning
- Clear conversation memory
- Logout with session memory reset
- Web-based chat interface
- REST API
- Swagger/OpenAPI documentation
- Automated tests
- SQLite database

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Passlib / bcrypt
- Groq API
- Llama 3.3 70B
- HTML
- CSS
- JavaScript
- Pytest

## Project Structure

```text
Project-1-Custom-AI-Chatbot/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   └── chat.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   │
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── models.py
│   │   │
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   │       ├── ai/
│   │       ├── auth_service.py
│   │       ├── chat_service.py
│   │       └── memory.py
│   │
│   └── tests/
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── js/
│
├── tests/
├── .env
├── .gitignore
└── README.md
````

## Architecture

The application follows a modular backend architecture:

```text
User
 │
 ▼
Web Frontend
 │
 ▼
FastAPI REST API
 │
 ├── Authentication
 │      └── JWT
 │
 ├── Chat API
 │      ├── Chat Service
 │      ├── Conversation Memory
 │      └── Groq AI Client
 │
 └── Database Layer
        ├── Repository
        └── SQLite
```

## Authentication

Users can:

1. Create an account.
2. Login with username and password.
3. Receive a JWT access token.
4. Use the token to access protected chat endpoints.
5. Logout and clear the current in-memory conversation.

Passwords are hashed before being stored.

## Conversation Memory

The chatbot uses **session-based in-memory conversation memory**.

The memory contains:

* System prompt
* User messages
* Assistant responses

Only the latest two conversation turns are retained.

Conversation memory can be cleared using the **Clear Chat** button.

Logging out also clears the user's in-memory conversation.

The conversation memory is intentionally not stored permanently in the database.

## LLM Integration

The chatbot uses the Groq API with:

```text
Model: llama-3.3-70b-versatile
```

The API key is loaded from the `.env` file.

## API Endpoints

### Authentication

```text
POST /auth/signup
POST /auth/login
```

### Chat

```text
POST /chat
POST /chat/clear
```

### Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Setup

### 1. Create virtual environment

```powershell
py -3.12 -m venv .venv
```

### 2. Activate virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secure_secret_key
```

Never commit `.env` to GitHub.

### 5. Start the backend

```powershell
cd backend
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### 6. Open the frontend

Open:

```text
frontend/login.html
```

in a browser.

## Testing

Run the complete automated test suite:

```powershell
pytest -v
```

Current test suite:

```text
10 tests passed
```

The tests cover:

* Password hashing and verification
* Conversation memory creation
* Conversation storage
* Memory clearing
* Conversation pruning
* Chat service behavior
* AI failure handling

## Security

* Passwords are hashed using bcrypt.
* JWT tokens protect authenticated endpoints.
* API credentials are loaded from environment variables.
* `.env` must not be committed.
* Database files should not be committed.
* Protected endpoints require authentication.

## Error Handling

The application handles authentication failures and AI service failures.

If the AI service becomes unavailable, the API returns a service-unavailable response instead of exposing internal implementation details.

## Project Objective

This project demonstrates the development of a complete conversational AI application using an LLM API, authentication, session-based memory, REST APIs, database persistence, a web interface, and automated testing.

```

### After pasting

1. Press **Ctrl + S**
2. Close Notepad.
3. **Do not run anything else yet.**
4. Tell me **"README done"**.

Then I'll give you **only the next step**.
```
