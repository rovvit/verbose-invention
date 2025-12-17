from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import timezone
from aiogram import Bot
from utils.logger import logger
from services.notification import notify_expiring_subscriptions
from config import SCHEDULER_HOUR, SCHEDULER_MINUTE

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
        notify_expiring_subscriptions,
        trigger=CronTrigger(hour=SCHEDULER_HOUR, minute=SCHEDULER_MINUTE, timezone=timezone.utc),
        kwargs={"bot": bot, "days": 1},
        id="notify_expiring_subscriptions_1",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(f"[STARTUP] Scheduler started, added job at {SCHEDULER_HOUR}:{SCHEDULER_MINUTE} UTC")

async def on_shutdown(bot: Bot):
    global scheduler
    if scheduler:
        logger.info("[SHUTDOWN] Shutting down scheduler")
        scheduler.shutdown()
