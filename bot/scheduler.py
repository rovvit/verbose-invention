from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import timezone

from services.notification import notify_expiring_subscriptions

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone=timezone.utc)

    scheduler.add_job(
        notify_expiring_subscriptions,
        trigger=CronTrigger(hour=9, minute=0),  # 09:00 GMT
        kwargs={
            "bot": bot,
            "days": 5,
        },
        id="notify_expiring_subscriptions",
        replace_existing=True,
    )

    scheduler.start()

    return scheduler
