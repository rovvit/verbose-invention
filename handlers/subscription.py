from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states import AppState
from services.subscription import check_subscription
from telegram.invites import create_invite
from utils.keyboards import check_by_email_keyboard, main_menu_keyboard
from utils.messages import (
    CHECK_EMAIL,
    SUBSCRIPTION_FOUND,
    SUBSCRIPTION_FOUND_BUT_LINK_FAILED,
    SUBSCRIPTION_NOT_FOUND,
)
from utils.logger import logger
from services.ban import unban_user

router = Router()

@router.callback_query(F.data == "check_subscription", StateFilter(None))
async def check_by_username(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    username = callback.from_user.username
    user_id = callback.from_user.id
    logger.info(f"[CHECK] user_id={user_id} username={username}")

    if username:
        payment = await check_subscription(
            username=username,
            telegram_user_id=user_id,
        )
        if payment:
            await unban_user(bot=callback.bot, user_id=user_id)
            await success_payment(callback.message, state, callback.bot)
            return

    await state.set_state(AppState.check_by_email)
    await callback.message.edit_text(CHECK_EMAIL)

@router.message(StateFilter(AppState.check_by_email))
async def check_by_email(message: types.Message, state: FSMContext):
    email = message.text.strip().lower()
    user_id = message.from_user.id

    logger.info(f"[CHECK] user_id={user_id} email={email}")

    msg = await message.answer("Проверяю оплату...")
    payment = await check_subscription(
        email=email,
        telegram_user_id=user_id,
    )

    if payment:
        await unban_user(bot=message.bot, user_id=user_id)
        await success_payment(msg, state, message.bot)
    else:
        await msg.edit_text(
            SUBSCRIPTION_NOT_FOUND,
            reply_markup=check_by_email_keyboard(),
        )
        await state.clear()

async def success_payment(
    message: types.Message,
    state: FSMContext,
    bot,
):
    try:
        invite = await create_invite(bot)
        await message.edit_text(f"{SUBSCRIPTION_FOUND} {invite}")
        await state.clear()
    except Exception:
        await message.edit_text(
            SUBSCRIPTION_FOUND_BUT_LINK_FAILED,
            reply_markup=check_by_email_keyboard(),
        )
