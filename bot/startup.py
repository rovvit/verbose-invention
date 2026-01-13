from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import timezone
from aiogram import Bot

from services.ban import ban_expired_subscriptions
from utils.admin_log import log_start
from utils.logger import logger
from services.notification import notify_expiring_subscriptions
from config import SCHEDULER_HOUR, SCHEDULER_MINUTE, BAN_HOUR, BAN_MINUTE

scheduler = None

async def on_startup(bot: Bot):
    """
    Startup function:
    - Runs APScheduler
    - Adds job for notifications
    """
    global scheduler
    logger.info("[STARTUP] Bot is starting")

    scheduler = AsyncIOScheduler(timezone=timezone.utc)

    scheduler.add_job(
        notify_expiring_subscriptions,
        trigger=CronTrigger(hour=SCHEDULER_HOUR, minute=SCHEDULER_MINUTE, timezone=timezone.utc),
        kwargs={"bot": bot, "days": 5},
        id="notify_expiring_subscriptions_5",
        replace_existing=True,
    )

    scheduler.add_job(
        ban_expired_subscriptions,
        trigger=CronTrigger(hour=BAN_HOUR, minute=BAN_MINUTE, timezone=timezone.utc),
        kwargs={"bot": bot},
        id="ban_expired",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(f"[STARTUP] Scheduler started, added notification job at {SCHEDULER_HOUR}:{SCHEDULER_MINUTE} UTC")
    logger.info(f"[STARTUP] Scheduler started, added ban job at {BAN_HOUR}:{BAN_MINUTE} UTC")
    await log_start(bot)

async def on_shutdown(bot: Bot):
    global scheduler
    if scheduler:
        logger.info("[SHUTDOWN] Shutting down scheduler")
        scheduler.shutdown()
