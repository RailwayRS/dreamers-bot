import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# Печать значения строки подключения
logging.debug(f"Строка подключения к базе данных: {settings.database_url}")

try:
    # Создание подключения к базе данных
    engine = create_async_engine(settings.database_url, echo=False)
    logging.debug("Подключение к базе данных успешно.")
except Exception as e:
    logging.error(f"Ошибка при подключении к базе данных: {e}")

# Создание сессии
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

