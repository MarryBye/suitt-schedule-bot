import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file from project root if it exists
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
GROUP_ID: str = os.getenv("GROUP_ID", "0")
GEMINI_API_TOKEN: str = os.getenv("GEMINI_API_TOKEN", "")
GEMINI_USED_MODEL: str = os.getenv("GEMINI_USED_MODEL", "gemini-1.5-flash")
SQLITE_DBFILE: str = os.getenv("SQLITE_DBFILE", "schedule.db")
