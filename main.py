import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN, TARGET_CHAT_ID
from states import AppState
from utils.keyboards import show_menu
from utils.messages import SUBSCRIPTION_NOT_FOUND, SUBSCRIPTION_FOUND, SUBSCRIPTION_FOUND_BUT_LINK_FAILED
from webhook_service import find_subscription
from utils.logger import logger

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"), StateFilter(None))
async def cmd_start(message: types.Message, state: FSMContext):
    logger.info(f"[START] New message from {message.from_user.id}")
    await show_menu(message, state)


@dp.message(Command("get_chat_id"), StateFilter(None))
async def get_chat_id(message: types.Message):
    await message.answer(f"chat_id этой группы: {message.chat.id}")


@dp.callback_query(F.data == "check_subscription", StateFilter(AppState.check_subscription))
async def check_subscription(callback: types.CallbackQuery, state: FSMContext):
    logger.info(f"[CHECK] Checking subscription for {callback.from_user.username} by telegram_tag")
    payment = await find_subscription(telegram_tag=callback.from_user.username)
    if payment:
        await check_payment(callback.message)
    else:
        await state.set_state(AppState.check_by_email)
        await callback.message.answer(f"Введите email")
    await callback.answer()


@dp.message(StateFilter(AppState.check_by_email))
async def handle_email(message: types.Message):
    email = message.text.strip().lower()
    logger.info(f"[CHECK] Checking subscription for {email} by email")

    await message.answer("Проверяю оплату, пожалуйста подождите...")
    payment = await find_subscription(email=email)
    if payment:
        await check_payment(message)
    else:
        await message.answer(
            SUBSCRIPTION_NOT_FOUND
        )


async def check_payment(message: types.Message):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=int(TARGET_CHAT_ID))
        await message.answer(
            f"{SUBSCRIPTION_FOUND} {invite_link.invite_link}"
        )
    except Exception as e:
        await message.answer(SUBSCRIPTION_FOUND_BUT_LINK_FAILED)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
