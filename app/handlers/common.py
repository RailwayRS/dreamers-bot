from aiogram import Router, types, F
from app.database import SessionLocal
from app.models import User, Role
from sqlalchemy.future import select

router = Router()

@router.message(F.text == "/start")
async def cmd_start(msg: types.Message):
    async with SessionLocal() as db:
        result = await db.execute(select(User).filter_by(tg_id=msg.from_user.id))
        user = result.scalars().first()
        if not user:
            await msg.answer("Выберите роль:\n1 — мечтатель\n2 — исполнитель")
            return

    await msg.answer("Вы уже зарегистрированы. /profile для информации")

@router.message(F.text.in_(["1", "2"]))
async def choose_role(msg: types.Message):
    role = Role.DREAMER if msg.text == "1" else Role.EXECUTOR
    try:
        async with SessionLocal() as db:
            result = await db.execute(select(User).filter_by(tg_id=msg.from_user.id))
            user = result.scalars().first()

            if user:
                # Если пользователь уже существует, обновляем его роль
                user.role = role
                db.add(user)
            else:
                # Если пользователя нет, создаём нового
                db.add(User(tg_id=msg.from_user.id, role=role, balance=1))

            await db.commit()  # Сохраняем изменения

        await msg.answer(f"Регистрация завершена как {role.name.lower()}! Баланс: 1 монета")
    except IntegrityError as e:
        await msg.answer("Произошла ошибка при регистрации. Попробуйте позже.")
        print(e)


