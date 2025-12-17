

from aiogram import Bot
from utils.logger import logger

async def on_startup(bot: Bot):
    logger.info("[STARTUP] Bot is starting")

    # here later:
    # - scheduler.start()
    # - http_client.start()

    logger.info("[STARTUP] Startup completed")