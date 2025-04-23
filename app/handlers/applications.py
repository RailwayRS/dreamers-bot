from aiogram import Router, F, types
from app.database import SessionLocal
from app.models import Application, AppStatus
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class ApplyStates(StatesGroup):
    waiting_text = State()

@router.callback_query(F.data.startswith("apply:"))
async def ask_apply(call: types.CallbackQuery, state: FSMContext):
    card_id = int(call.data.split(":")[1])
    await state.set_state(ApplyStates.waiting_text)
    await state.update_data(card_id=card_id)
    await call.message.answer(
        "✍️ Напиши, почему ты достоин этой мечты. Отправь одним сообщением.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_apply")]
        ])
    )

@router.message(ApplyStates.waiting_text)
async def save_application(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    card_id = data["card_id"]
    async with SessionLocal.begin() as db:
        db.add(Application(card_id=card_id, user_id=msg.from_user.id, text=msg.text))
    await msg.answer("✅ Заявка отправлена! Ждите ответа исполнителя.")
    await state.clear()
