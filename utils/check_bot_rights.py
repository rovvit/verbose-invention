import asyncio
from aiogram import Bot
from config import TARGET_CHAT_ID, TELEGRAM_BOT_TOKEN


async def main():
    bot = Bot(TELEGRAM_BOT_TOKEN)

    me = await bot.get_me()
    member = await bot.get_chat_member(TARGET_CHAT_ID, me.id)

    print("\n=== BOT INFO ===")
    print(f"id: {me.id}")
    print(f"username: @{me.username}")
    print(f"chat_id: {TARGET_CHAT_ID}")

    print("\n=== MEMBERSHIP STATUS ===")
    print(f"status: {member.status}")

    if member.status != "administrator":
        print("\nBot is NOT an admin in this chat — ban will NOT work")
        return

    print("\n=== ADMIN RIGHTS ===")

    rights = [
        "can_manage_chat",
        "can_delete_messages",
        "can_restrict_members",
        "can_promote_members",
        "can_invite_users",
        "can_pin_messages",
        "can_manage_topics",
    ]

    for r in rights:
        print(f"{r}: {getattr(member, r, False)}")


if __name__ == "__main__":
    asyncio.run(main())