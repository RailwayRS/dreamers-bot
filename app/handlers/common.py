from aiogram import Router, types, F
from app.database import SessionLocal
from app.models import User, Role

router = Router()

@router.message(F.text == "/start")
async def cmd_start(msg: types.Message):
    async with SessionLocal() as db:
        user = await db.get(User, msg.from_user.id)  # Добавляем await для асинхронного получения
        if not user:
            await msg.answer("Выберите роль:\n1 — мечтатель\n2 — исполнитель")
            return

    await msg.answer("Вы уже зарегистрированы. /profile для информации")

@router.message(F.text.in_(["1", "2"]))
async def choose_role(msg: types.Message):
    role = Role.DREAMER if msg.text == "1" else Role.EXECUTOR
    async with SessionLocal.begin() as db:
        db.add(User(tg_id=msg.from_user.id, role=role, balance=1))
    await msg.answer(f"Регистрация завершена как {role.name.lower()}! Баланс: 1 монета")

