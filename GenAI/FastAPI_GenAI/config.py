import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load Environment Variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

# Gemini Client
client = genai.Client(api_key=api_key)

# Gemini Model
MODEL_NAME = "gemini-3-flash-preview"