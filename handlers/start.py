from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from utils.keyboards import main_menu_keyboard
from utils.messages import START_MESSAGE
from utils.logger import logger

router = Router()

# Ignores groups messages
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def ignore_groups(message: types.Message):
    logger.info(f"Skip message for {message.chat.type}")
    return

async def show_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        START_MESSAGE,
        reply_markup=main_menu_keyboard()
    )

@router.message(Command("start"), StateFilter(None))
async def cmd_start(message: types.Message, state: FSMContext):
    logger.info(f"[START] New message from {message.from_user.id}")
    await show_menu(message, state)

@router.message(Command("get_chat_id"), StateFilter(None))
async def get_chat_id(message: types.Message):
    await message.answer(f"chat_id этой группы: {message.chat.id}")

@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await callback.answer()
    await callback.message.edit_text(
        START_MESSAGE,
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()