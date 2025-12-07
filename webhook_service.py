from aiogram.client.session import aiohttp
from config import STRIPE_WEBHOOK_HOST
from utils.logger import logger


async def find_subscription(email: str=None, telegram_tag: str=None):
    api_url = f"http://{STRIPE_WEBHOOK_HOST}/api/check_subscription"
    async with aiohttp.ClientSession() as session:
        if email:
            logger.info(f"[WH SERVICE] Checking by email {email}")
            async with session.get(
                api_url, params={"email": email}
            ) as resp:
                data = await resp.json()
                return data["paid"] == "active" #TODO Implement logic for non-active statuses
        elif telegram_tag:
            logger.info(f"[WH SERVICE] Checking by telegram_tag {telegram_tag}")
            async with session.get(
                    api_url, params={"telegram_tag": telegram_tag}
            ) as resp:
                data = await resp.json()
                return data["paid"] == "active" #TODO Implement logic for non-active statuses
        else:
            logger.error(f"[WH SERVICE] No argument passed for checking")
            return False

