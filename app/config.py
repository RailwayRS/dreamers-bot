
from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()
@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    admin_ids: list[int] = [int(x) for x in os.getenv("ADMINS", "").split(",") if x]
settings = Settings()
