import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError
    {
        "!!!! OpenAI Key Not Found !!!!"
        "Make sure .env has the key"
    }
