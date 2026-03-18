import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. "
        "Create a .env file in this folder with: OPENAI_API_KEY=sk-your-key-here"
    )