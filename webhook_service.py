from aiogram.client.session import aiohttp
from config import STRIPE_WEBHOOK_HOST
from utils.logger import logger


async def find_subscription(email: str=None, username: str=None, telegram_user_id: int=None):
    api_url = f"http://{STRIPE_WEBHOOK_HOST}/api/subscription/check"
    payload = {"user_id": telegram_user_id}
    if email:
        payload["email"] = email
        logger.info(f"[WH SERVICE] Checking by email {email} for user {telegram_user_id}")
    elif username:
        payload["username"] = username
        logger.info(f"[WH SERVICE] Checking by telegram_tag {username} for user {telegram_user_id}")
    else:
        logger.error(f"[WH SERVICE] No argument passed for checking for user {telegram_user_id}")
        return False

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload) as resp:
            try:
                data = await resp.json()
            except Exception:
                logger.exception(f"[WH SERVICE] Failed to parse JSON response for user {telegram_user_id}")
                return False

            logger.info(f"[WH SERVICE] Response is {data}")
            return data.get("subscription_status", False)
