import asyncio
import logging
import traceback

from aiogram import Bot
from datetime import datetime, timezone

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

    today = datetime.now(timezone.utc).date()

    for item in subscriptions:
        user_id = item["user_id"]
        raw_end_date = item["date_end"]

        try:
            if isinstance(raw_end_date, str):
                end_date = datetime.fromisoformat(raw_end_date).date()
            elif isinstance(raw_end_date, datetime):
                end_date = raw_end_date.date()
            else:
                end_date = raw_end_date

            diff_days = (end_date - today).days

            logger.info(
                f"[SCHEDULER] user={user_id} end_date={end_date} diff={diff_days}"
            )

            if diff_days == 0:
                await bot.send_message(chat_id=user_id, text=REMINDER_TODAY)

            elif diff_days == 4:
                await bot.send_message(chat_id=user_id, text=REMINDER_5_DAYS)

            else:
                logger.info(
                    f"[SCHEDULER] Skipping user {user_id}, diff={diff_days}"
                )

            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(
                "[SCHEDULER] Failed to notify user "
                f"user_id={user_id} end_date={raw_end_date} "
                f"diff_days={locals().get('diff_days', 'N/A')} "
                f"error={repr(e)}\n{traceback.format_exc()}"
            )
