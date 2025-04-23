from app.handlers import applications

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
    dp.include_router(common.router)
    await on_startup()
    dp.include_router(applications.router)

    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
