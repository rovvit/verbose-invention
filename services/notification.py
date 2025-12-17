import asyncio
import logging
from datetime import datetime, timezone

from aiogram import Bot

from services.subscription import get_expiring_subscriptions

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

    now = datetime.now(timezone.utc)

    for item in subscriptions:
        try:
            user_id = item["user_id"]
            date_end = datetime.fromisoformat(item["date_end"])

            days_left = max((date_end - now).days, 0)

            await bot.send_message(
                chat_id=user_id,
                text=(
                    "⚠️ Ваша подписка скоро закончится\n\n"
                    f"Дата окончания: {date_end:%d.%m.%Y}\n"
                    f"Осталось дней: {days_left}"
                )
            )

            await asyncio.sleep(0.1)  # антифлуд

        except Exception:
            logger.exception(
                f"[SCHEDULER] Failed to notify user {item}"
            )
