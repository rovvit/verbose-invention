import time
from aiogram import Bot
from config import TARGET_CHAT_ID

async def create_invite(bot: Bot) -> str:
    chat = await bot.get_chat(TARGET_CHAT_ID)
    target_chat_id = TARGET_CHAT_ID # chat.linked_chat_id or TARGET_CHAT_ID
    invite = await bot.create_chat_invite_link(
        chat_id=int(target_chat_id),
        expire_date=int(time.time()) + 24 * 60 * 60,
        member_limit=1,
    )
    return invite.invite_link