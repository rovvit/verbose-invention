import asyncio

from bot.dispatcher import bot, dp
from bot.startup import on_startup, on_shutdown
from handlers import start, subscription, fallback

dp.include_router(start.router)
dp.include_router(subscription.router)
dp.include_router(fallback.router)

async def main():
    await on_startup(bot)
    await dp.start_polling(bot, on_shutdown=on_shutdown)

if __name__ == "__main__":
    asyncio.run(main())