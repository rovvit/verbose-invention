from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import timezone
from aiogram import Bot
from utils.logger import logger
from services.notification import notify_expiring_subscriptions

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
        trigger=CronTrigger(hour=10, minute=0),
        kwargs={"bot": bot, "days": 5},
        id="notify_expiring_subscriptions",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("[STARTUP] Scheduler started")

async def on_shutdown(bot: Bot):
    global scheduler
    if scheduler:
        logger.info("[SHUTDOWN] Shutting down scheduler")
        scheduler.shutdown()
