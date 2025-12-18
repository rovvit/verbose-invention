from aiogram import Bot
from utils.logger import logger
from services.subscription import mark_banned, get_expiring_subscriptions
from config import TARGET_CHAT_ID
from datetime import datetime, timezone
import asyncio

async def ban_expired_subscriptions(bot: Bot):
    users = await get_expiring_subscriptions(days=1, end_date=datetime.now(timezone.utc).date())
    logger.info(f"[BAN] Starting baning users...")
    for u in users:
        await ban_user(
            bot=bot,
            user_id=u["user_id"]
        )

async def ban_user(bot: Bot, user_id: int):
    for attempt in range(3):
        try:
            await bot.ban_chat_member(TARGET_CHAT_ID, user_id)
            await mark_banned(user_id)
            logger.info(f"[BAN] User {user_id} banned")
            return
        except Exception:
            logger.exception(f"[BAN] Failed to ban {user_id}, attempt {attempt+1}")
            await asyncio.sleep(1)