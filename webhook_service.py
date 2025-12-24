from aiogram.client.session import aiohttp
from config import STRIPE_WEBHOOK_HOST
from utils.logger import logger
from datetime import datetime


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

async def get_expiring_subscriptions(days: int=5, end_date: datetime.date = datetime.today().strftime("%Y-%m-%d")):
    api_url = f"http://{STRIPE_WEBHOOK_HOST}/api/subscription/expiring"
    async with aiohttp.ClientSession()as session:
        params = {"days": days, "end_date": end_date}
        params = {k: v for k, v in params.items() if v is not None}
        async with session.get(api_url, params=params) as resp:
            try:
                data = await resp.json()
                logger.info(f"[WH GET EXP SUB] Got this data {data}")
                return data
            except Exception:
                logger.exception(f"[WH SERVICE] get_expiring_subscriptions error")
                logger.exception(Exception)
                return []


async def post_mark_banned(user_id: int):
    async with aiohttp.ClientSession() as session:
        await session.post(
            f"http://{STRIPE_WEBHOOK_HOST}/api/subscription/ban",
            json={"user_id": user_id}
        )