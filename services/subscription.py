from datetime import datetime

import webhook_service as wh

async def check_subscription(username=None, email=None, telegram_user_id=None, name=None):
    return await wh.find_subscription(
        username=username,
        email=email,
        telegram_user_id=telegram_user_id,
        name=name
    )

async def get_expiring_subscriptions(days: int=5, start_date: datetime.date = None):
    return await wh.get_expiring_subscriptions(days=days, start_date=start_date)

async def mark_banned(user_id: int):
    return await wh.post_mark_banned(user_id)