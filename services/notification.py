import asyncio
import logging

from aiogram import Bot

from services.subscription import get_expiring_subscriptions
from utils.messages import REMINDER_5_DAYS, REMINDER_TODAY

logger = logging.getLogger(__name__)

async def notify_expiring_subscriptions(
    bot: Bot,
    days: int = 5,
):
    logger.info("[SCHEDULER] Checking expiring subscriptions")

    subscriptions = await get_expiring_subscriptions(days=days)

    if not subscriptions:
        logger.info("[SCHEDULER] No expiring subscriptions")
        return


    for item in subscriptions:
        try:
            user_id = item["user_id"]
            if days == 1:
                await bot.send_message(
                    chat_id=user_id,
                    text=REMINDER_TODAY
            )
            elif days == 5:
                await bot.send_message(
                    chat_id=user_id,
                    text=REMINDER_5_DAYS
                )
            else:
                logger.info("[SCHEDULER] Other than 5 or 1 days is passed, skipping.")
            await asyncio.sleep(0.1)

        except Exception:
            logger.exception(
                f"[SCHEDULER] Failed to notify user {item}"
            )
