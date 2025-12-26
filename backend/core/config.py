import os
from pathlib import Path
from pydantic_settings import BaseSettings

APP_DIR = Path(os.getcwd())
DATA_DIR = Path.home() / ".chimera_enterprise_data"
DATA_DIR.mkdir(exist_ok=True)

SCREENSHOT_DIR = APP_DIR / "backend/static/screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    # Browser
    CHIMERA_HEADLESS: bool = os.getenv("CHIMERA_HEADLESS", "false").lower() == "true"
    
    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:latest")  # change as needed

    # Computer Use Safety
    # If true, restrict goto() to these domains only (comma-separated). Empty means allow all.
    CHIMERA_ALLOWED_DOMAINS: str = os.getenv("CHIMERA_ALLOWED_DOMAINS", "")

settings = Settings()
