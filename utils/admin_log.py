import logging
from aiogram import Bot, types
from aiogram.utils.markdown import hbold, hcode, hitalic
from datetime import datetime
from config import ADMIN_CHAT_ID, SCHEDULER_HOUR, SCHEDULER_MINUTE, BAN_HOUR, BAN_MINUTE

async def log_start(bot: Bot):
    """Уведомление о запуске бота или планировщика"""
    message = f"""
    🚀 **Бот запущен.**
    Настройки Scheduler 
    **Notifications**: {SCHEDULER_HOUR}:{SCHEDULER_MINUTE} UTC
    **Bans**: {BAN_HOUR}:{BAN_MINUTE} UTC 
    """
    try:
        await bot.send_message(ADMIN_CHAT_ID, message, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка логирования log_start: {e}")


from aiogram import Bot, types


async def log_command_start(bot: Bot, message: types.Message):
    """Уведомление в админ-чат о том, что пользователь нажал /start"""
    user = message.from_user

    # Собираем информацию о пользователе максимально подробно для заказчика
    full_name = user.full_name
    username = f"@{user.username}" if user.username else "нет username"
    user_id = user.id

    log_text = (
        f"👤 **Новый пользователь в боте!**\n\n"
        f"**Имя:** {full_name}\n"
        f"**Username:** {username}\n"
        f"**ID:** `{user_id}`\n"
        f"**Действие:** нажал /start"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=log_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Ошибка логирования log_command_start: {e}")


async def log_check(bot: Bot, user: types.User, email: str, status: str):
    """
    Лог ручной проверки подписки.
    Передаем объект user (из message или callback_query).
    """
    username = f"@{user.username}" if user.username else "нет username"
    full_name = user.full_name

    # Если email не введен (проверка по username), пишем об этом
    email_text = hcode(email) if email else hitalic("не указан (проверка по username)")
    result_text = "✅ Доступ разрешен" if status else "❌ Подписка не найдена"

    log_text = (
        f"🔍 {hbold('Ручная проверка подписки')}\n\n"
        f"👤 {hbold('Пользователь:')} {full_name} ({username}); ID: {user.id}\n"
        f"📧 {hbold('Email:')} {email_text}\n"
        f"📊 {hbold('Результат:')} {result_text}"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=log_text,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Ошибка логирования log_check: {e}")


async def log_notification(bot: Bot, user_data: dict, days_left: int):
    """
    Уведомление в админ-чат об отправке автоматического напоминания.
    :param user_data: Словарь с ключами 'full_name', 'username', 'date_end'
    :param days_left: Сколько дней осталось (0 или 5)
    """
    if days_left == 0:
        status_label = "🔴 ПОСЛЕДНЕЕ ПРЕДУПРЕЖДЕНИЕ (Сегодня)"
    else:
        status_label = f"🟡 Напоминание за {days_left} дн."

    raw_date = user_data.get('date_end')
    formatted_date = "Неизвестно"

    try:
        if isinstance(raw_date, str):
            dt_obj = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
            formatted_date = dt_obj.strftime('%d.%m.%Y %H:%M')
        elif isinstance(raw_date, datetime):
            formatted_date = raw_date.strftime('%d.%m.%Y %H:%M')
    except Exception as e:
        logging.error(f"Ошибка форматирования даты: {e}")
        formatted_date = str(raw_date)

    log_text = (
        f"📩 {hbold('Авто-уведомление отправлено')}\n"
        f"────────────────────\n"
        f"👤 {hbold('Клиент:')} {user_data['full_name']} ({user_data['username']} ID: {user_data['user_id']})\n"
        f"📅 {hbold('Дата окончания:')} {formatted_date}\n"
        f"📊 {hbold('Статус:')} {status_label}\n"
        f"────────────────────\n"
        f"✅ {hitalic('Бот успешно доставил сообщение в ЛС')}"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=log_text,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Ошибка логирования log_notification: {e}")

async def log_ban(bot: Bot, member: types.ChatMember, success: bool):
    """Отчет об удалении пользователя из канала"""
    status = "🚫 Удален из канала" if success else "⚠️ Ошибка при удалении"
    user = member.user
    full_name = user.full_name
    username = f"@{user.username}" if user.username else "нет username"
    user_id = user.id

    message = (
        f"{status}\n"
        f"👤 Клиент: {full_name} {username}, ID: {user_id}"
    )
    try:
        await bot.send_message(ADMIN_CHAT_ID, message, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка логирования log_ban: {e}")