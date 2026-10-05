import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")
    AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
    AI_BASE_URL = os.getenv("AI_BASE_URL", "").strip() or None
    AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
    IMAGE_MODEL = os.getenv("IMAGE_MODEL", "dall-e-3")
    AI_TIMEOUT = float(os.getenv("AI_TIMEOUT", "60"))
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
