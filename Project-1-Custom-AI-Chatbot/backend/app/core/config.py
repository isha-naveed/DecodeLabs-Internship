from pathlib import Path
import os
from dotenv import load_dotenv

# Project root (backend/)
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env
load_dotenv(BASE_DIR / ".env")

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")