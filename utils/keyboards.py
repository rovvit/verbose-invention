from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states import AppState

async def show_menu(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()

    builder.button(text="Проверить подписку", callback_data="check_subscription")
    await message.answer(
        "Добро пожаловать в бота! Чем могу помочь?",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AppState.check_subscription)
