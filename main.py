import asyncio
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN, TARGET_CHAT_ID, TELEGRAM_CHAT_LINK
from states import AppState
from utils.error_handler import errors_router
from utils.keyboards import main_menu_keyboard, check_by_email_keyboard
from utils.messages import SUBSCRIPTION_NOT_FOUND, SUBSCRIPTION_FOUND, SUBSCRIPTION_FOUND_BUT_LINK_FAILED, \
    START_MESSAGE, CHECK_EMAIL
from webhook_service import find_subscription
from utils.logger import logger

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(errors_router)

async def show_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(START_MESSAGE,
        reply_markup=main_menu_keyboard()
    )

@dp.message(Command("start"), StateFilter(None))
async def cmd_start(message: types.Message, state: FSMContext):
    logger.info(f"[START] New message from {message.from_user.id}")
    await show_menu(message, state)


@dp.message(Command("get_chat_id"), StateFilter(None))
async def get_chat_id(message: types.Message):
    await message.answer(f"chat_id этой группы: {message.chat.id}")


@dp.callback_query(F.data == "check_subscription", StateFilter(None))
async def check_subscription(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    telegram_tag = callback.from_user.username
    logger.info(f"[CHECK] Checking subscription for {telegram_tag} by telegram_tag")

    if telegram_tag:
        payment = await find_subscription(telegram_tag=telegram_tag)
        if payment:
            await check_payment(callback.message, state)
            return

    await state.set_state(AppState.check_by_email)
    await callback.message.edit_text(f"{CHECK_EMAIL}")


@dp.message(StateFilter(AppState.check_by_email))
async def handle_email(message: types.Message, state: FSMContext):
    email = message.text.strip().lower()
    logger.info(f"[CHECK] Checking subscription for {email} by email")

    msg = await message.answer("Проверяю оплату, пожалуйста подождите...")
    payment = await find_subscription(email=email)
    if payment:
        await check_payment(msg, state)
    else:
        await msg.edit_text(SUBSCRIPTION_NOT_FOUND, reply_markup=check_by_email_keyboard())
        await state.clear()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(START_MESSAGE, reply_markup=main_menu_keyboard())

@dp.callback_query(F.data == "check_subscription")
async def stale_check_subscription(callback: types.CallbackQuery):
    await callback.answer()

@dp.message(StateFilter(None))
async def no_state_message(message: types.Message, state: FSMContext):
    logger.info(f"[NO STATE] No state filter reached, showing main menu")
    await show_menu(message, state)

async def check_payment(msg: types.Message, state: FSMContext):
    try:
        invite = await bot.create_chat_invite_link(
            chat_id=int(TARGET_CHAT_ID),
            expire_date=int(time.time()) + 24 * 60 * 60,  # ссылка будет действовать 24 часа
            member_limit=1,
        )
        # invite_link = TELEGRAM_CHAT_LINK  #TODO Remove later
        await msg.edit_text(
            f"{SUBSCRIPTION_FOUND} {invite.invite_link}"
        )
        await state.clear()
    except Exception as e:
        await msg.edit_text(SUBSCRIPTION_FOUND_BUT_LINK_FAILED, reply_markup=check_by_email_keyboard())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
