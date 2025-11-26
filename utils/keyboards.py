from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states import AppState
from utils.messages import START_MESSAGE


async def show_menu(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()

    builder.button(text="Проверить подписку", callback_data="check_subscription")
    await message.answer(START_MESSAGE,
        reply_markup=builder.as_markup()
    )
    await state.set_state(AppState.check_subscription)
