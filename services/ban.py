from aiogram import Bot
from utils.logger import logger
from services.subscription import mark_banned, get_expiring_subscriptions
from config import TARGET_CHAT_ID
from datetime import datetime, timezone
import asyncio

async def ban_expired_subscriptions(bot: Bot):
    users = await get_expiring_subscriptions(days=1, end_date=datetime.now(timezone.utc).date())
    logger.info(f"[BAN] Starting baning users... {users}")
    for u in users:
        if u["user_id"] == bot.id:
            logger.warning("[UNBAN] Skipping unban for bot itself")
        else:
            await ban_user(
                bot=bot,
                user_id=u["user_id"]
            )
            await asyncio.sleep(1000)

async def ban_user(bot: Bot, user_id: int):
    if user_id == bot.id:
        logger.warning("[BAN] Skipping ban for bot itself")
        return
    for attempt in range(3):
        try:
            chat = await bot.get_chat(TARGET_CHAT_ID)
            target_chat_id = chat.linked_chat_id or TARGET_CHAT_ID

            # logger.info(
            #     f"[BAN] chat_type={chat.type}, target_chat_id={target_chat_id}, "
            #     f"TARGET_CHAT_ID={TARGET_CHAT_ID}"
            # )

            member = await bot.get_chat_member(TARGET_CHAT_ID, user_id)
            logger.info(f"[BAN] member status before ban: {member.status}")

            await bot.ban_chat_member(TARGET_CHAT_ID, user_id)
            await mark_banned(user_id)

            logger.info(f"[BAN] User {user_id} banned")
            return
        except Exception:
            logger.exception(f"[BAN] Failed to ban {user_id}, attempt {attempt+1}")
            await asyncio.sleep(100)

async def unban_user(bot: Bot, user_id: int) -> None:
    if user_id == bot.id:
        logger.warning("[UNBAN] Skipping unban for bot itself")
        return
    try:
        chat = await bot.get_chat(TARGET_CHAT_ID)
        target_chat_id = chat.linked_chat_id or TARGET_CHAT_ID

        bot_member = await bot.get_chat_member(chat_id=target_chat_id, user_id=bot.id)
        if bot_member.status not in ["administrator", "creator"]:
            logger.error("[UNBAN] Bot is not admin or lost permissions!")
        else:
            member = await bot.get_chat_member(chat_id=target_chat_id, user_id=user_id)
            logger.info(
                f"[UNBAN] Unbanning member: user_id={user_id}, status={member.status}"
            )

            await bot.unban_chat_member(chat_id=target_chat_id, user_id=user_id, only_if_banned=True)
            await bot.unban_chat_member(chat_id=TARGET_CHAT_ID, user_id=user_id, only_if_banned=True)
            logger.info(f"[UNBAN] Unbanned user {user_id}")
    except Exception as e:
        logger.exception(f"[UNBAN] Failed for user {user_id}")
        logger.exception(repr(e))