import time
from aiogram import Bot
from config import LINKED_CHAT_ID

async def create_invite(bot: Bot) -> str:
    invite = await bot.create_chat_invite_link(
        chat_id=int(LINKED_CHAT_ID),
        expire_date=int(time.time()) + 24 * 60 * 60,
        member_limit=1,
    )
    return invite.invite_link