import webhook_service as wh

async def check_subscription(username=None, email=None, telegram_user_id=None):
    return await wh.find_subscription(
        username=username,
        email=email,
        telegram_user_id=telegram_user_id,
    )

async def get_expiring_subscriptions(days: int=5):
    return await wh.get_expiring_subscriptions(days=days)