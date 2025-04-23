from app.handlers import applications, start  # Добавил импорт start

import asyncio, logging
from aiogram import Bot, Dispatcher
from app.config import settings
from app.handlers import common
from app.models import Base
from app.database import engine

async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    # Подключаем роутеры (хендлеры)
    dp.include_router(common.router)
    dp.include_router(start.router)  # Подключаем start
    dp.include_router(applications.router)

    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

