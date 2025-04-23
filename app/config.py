# app/config.py
from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    admin_ids: list[int] = field(
        default_factory=lambda: [
            int(x) for x in os.getenv("ADMINS", "").split(",") if x
        ]
    )

settings = Settings()

# Выводим значение переменной DATABASE_URL для проверки
print(settings.database_url)  # Эта строка выводит URL базы данных в консоль

