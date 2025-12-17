import asyncio

from bot.dispatcher import bot, dp
from handlers import start, subscription, fallback

dp.include_router(start.router)
dp.include_router(subscription.router)
dp.include_router(fallback.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())