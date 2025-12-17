from webhook_service import find_subscription

async def check_subscription(username=None, email=None, telegram_user_id=None):
    return await find_subscription(
        username=username,
        email=email,
        telegram_user_id=telegram_user_id,
    )