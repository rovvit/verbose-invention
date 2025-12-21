import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from aiogram import Bot
from config import TELEGRAM_BOT_TOKEN
from utils.logger import logger

default_text = """
Здравствуйте!
Данные о вашей подписке обновлены, пожалуйста, повторите проверку для получения приглашения на закрытый канал.

Команда клуба OutoSuomi 
"""

async def send_message(user_id: int, text: str=default_text):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    logger.info(f"[MANUAL SCRIPT] Send Message to {user_id} about {text}")
    try:
        await bot.send_message(chat_id=user_id, text=text)
        logger.info(f"[MANUAL SCRIPT] SUSCCESS Message sent to {user_id}")
    except Exception:
        logger.exception(f"[MANUAL SCRIPT] Something went wrong")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_message.py <user_id> <text>")
        sys.exit(1)

    user_id = int(sys.argv[1])
    # text = " ".join(sys.argv[2:])

    asyncio.run(send_message(user_id))
