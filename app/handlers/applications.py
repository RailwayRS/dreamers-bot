from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.database import SessionLocal
from app.models import User, Role, Task, Response
router = Router()

# Команда /start
@router.message(F.text == "/start")
async def cmd_start(msg: types.Message):
    async with SessionLocal() as db:
        user = await db.get(User, msg.from_user.id)
        if not user:
            # Если пользователя нет, предлагается выбрать роль
            markup = InlineKeyboardMarkup(row_width=1)
            button_dreamer = InlineKeyboardButton("1 — Мечтатель", callback_data="role_dreamer")
            button_executor = InlineKeyboardButton("2 — Исполнитель", callback_data="role_executor")
            markup.add(button_dreamer, button_executor)
            await msg.answer("Выберите роль:\n1 — Мечтатель\n2 — Исполнитель", reply_markup=markup)
            return
    await msg.answer("Вы уже зарегистрированы. Для изменения роли используйте /reset. /profile для информации.")

# Обработчик выбора роли (мечтатель или исполнитель)
@router.callback_query(F.data == "role_dreamer")
async def choose_role_dreamer(callback_query: types.CallbackQuery):
    await set_user_role(callback_query, Role.DREAMER)

@router.callback_query(F.data == "role_executor")
async def choose_role_executor(callback_query: types.CallbackQuery):
    await set_user_role(callback_query, Role.EXECUTOR)

async def set_user_role(callback_query: types.CallbackQuery, role: Role):
    async with SessionLocal() as db:
        user = await db.get(User, callback_query.from_user.id)
        if not user:
            # Если пользователя нет, создаём нового
            db.add(User(tg_id=callback_query.from_user.id, role=role, balance=1))
            await db.commit()
            await callback_query.message.answer(f"Регистрация завершена как {role.name.lower()}! Баланс: 1 монета")
        else:
            await callback_query.message.answer("Вы уже зарегистрированы.")
    await callback_query.answer()

# Кнопка для сброса роли
@router.message(F.text == "/reset")
async def reset_role(msg: types.Message):
    async with SessionLocal() as db:
        user = await db.get(User, msg.from_user.id)
        if user:
            markup = InlineKeyboardMarkup(row_width=1)
            reset_button = InlineKeyboardButton("Сбросить роль", callback_data="reset_role")
            markup.add(reset_button)
            await msg.answer("Нажмите кнопку для сброса роли:", reply_markup=markup)
        else:
            await msg.answer("Вы не зарегистрированы. Используйте /start для регистрации.")

# Обработка сброса роли через кнопку
@router.callback_query(F.data == "reset_role")
async def reset_role_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    async with SessionLocal() as db:
        user = await db.get(User, user_id)
        if user:
            # Сбрасываем роль
            user.role = None  # Очищаем роль
            db.add(user)
            await db.commit()
            await callback_query.message.answer("Ваша роль была сброшена. Теперь выберите новую роль с помощью команды /start.")
        else:
            await callback_query.message.answer("Пользователь не найден.")
    await callback_query.answer()  # Закрываем кнопку

# Команда /profile для получения информации о пользователе
@router.message(F.text == "/profile")
async def cmd_profile(msg: types.Message):
    async with SessionLocal() as db:
        user = await db.get(User, msg.from_user.id)
        if user:
            role = user.role.name if user.role else "Не назначена"
            balance = user.balance
            await msg.answer(f"Информация о пользователе:\nРоль: {role}\nБаланс: {balance} монет")
        else:
            await msg.answer("Вы не зарегистрированы. Используйте /start для регистрации.")

# Команда для создания задачи
@router.message(F.text.startswith("/create_task"))
async def create_task(msg: types.Message):
    task_data = msg.text[len("/create_task"):].strip()
    if not task_data:
        await msg.answer("Пожалуйста, предоставьте описание задачи после команды /create_task.")
        return

    async with SessionLocal() as db:
        task = Task(description=task_data, creator_id=msg.from_user.id)
        db.add(task)
        await db.commit()

    await msg.answer(f"Задача создана: {task_data}")

# Команда для получения списка задач
@router.message(F.text == "/tasks")
async def list_tasks(msg: types.Message):
    async with SessionLocal() as db:
        tasks = await db.execute(Task.select())
        tasks_list = tasks.fetchall()
        if tasks_list:
            task_text = "\n".join([f"Задача #{task.id}: {task.description}" for task in tasks_list])
            await msg.answer(f"Список задач:\n{task_text}")
        else:
            await msg.answer("Нет доступных задач.")

# Команда для отклика на задачу
@router.message(F.text.startswith("/response"))
async def response_task(msg: types.Message):
    try:
        task_id = int(msg.text[len("/response"):].strip())
    except ValueError:
        await msg.answer("Пожалуйста, укажите номер задачи после команды /response.")
        return

    async with SessionLocal() as db:
        task = await db.get(Task, task_id)
        if not task:
            await msg.answer("Задача не найдена.")
            return

        user = await db.get(User, msg.from_user.id)
        if not user or user.role != Role.EXECUTOR:
            await msg.answer("Вы должны быть исполнителем для отклика на задачу.")
            return

        # Создаем отклик
        response = Response(task_id=task.id, user_id=user.id)
        db.add(response)
        await db.commit()

    await msg.answer(f"Вы откликнулись на задачу #{task_id}.")

# Команда для получения откликов на задачу
@router.message(F.text.startswith("/responses"))
async def list_responses(msg: types.Message):
    try:
        task_id = int(msg.text[len("/responses"):].strip())
    except ValueError:
        await msg.answer("Пожалуйста, укажите номер задачи после команды /responses.")
        return

    async with SessionLocal() as db:
        task = await db.get(Task, task_id)
        if not task:
            await msg.answer("Задача не найдена.")
            return

        responses = await db.execute(Response.select().filter(Response.task_id == task.id))
        responses_list = responses.fetchall()
        if responses_list:
            response_text = "\n".join([f"Отклик от пользователя #{response.user_id}" for response in responses_list])
            await msg.answer(f"Отклики на задачу #{task_id}:\n{response_text}")
        else:
            await msg.answer("Нет откликов на эту задачу.")



