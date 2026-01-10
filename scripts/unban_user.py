import sys
import asyncio
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from services.ban import unban_user
from aiogram import Bot
from config import TELEGRAM_BOT_TOKEN
from utils.logger import logger

async def unban_user_script(user_id_arg: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    logger.info(f"[MANUAL SCRIPT] Unban {user_id_arg}")
    try:
        await unban_user(bot=bot, user_id=user_id_arg)
        logger.info(f"[MANUAL SCRIPT] SUCCESS Unbanned {user_id_arg}")
    except Exception:
        logger.exception(f"[MANUAL SCRIPT] Something went wrong")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unban.py <user_id>")
        sys.exit(1)

    user_id = int(sys.argv[1])

    asyncio.run(unban_user_script(user_id))