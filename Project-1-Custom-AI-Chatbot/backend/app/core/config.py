from pathlib import Path
import os
from dotenv import load_dotenv

# Project root (backend/)
BASE_DIR = Path(__file__).resolve().parents[3]
# Load .env
load_dotenv(BASE_DIR / ".env")

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY not found. Please check your .env file."
    )