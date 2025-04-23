from aiogram.utils.keyboard import InlineKeyboardBuilder

def card_actions(card_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="📩 Подать заявку", callback_data=f"apply:{card_id}")
    return kb.as_markup()
