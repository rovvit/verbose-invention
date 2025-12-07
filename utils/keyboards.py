from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states import AppState
from utils.messages import START_MESSAGE


def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить подписку", callback_data="check_subscription")
    return builder.as_markup()

def check_by_email_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Повторить попытку", callback_data="check_subscription")
    builder.button(text="Вернуться в главное меню", callback_data="back_to_main")
    return builder.as_markup()