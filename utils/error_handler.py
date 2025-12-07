from aiogram import Router
from aiogram.types import ErrorEvent
from utils.logger import logger

errors_router = Router()


@errors_router.error()
async def global_error_handler(event: ErrorEvent):
    exc = event.exception
    update = event.update

    logger.error(f"[ERROR HANDLER] Unhandled error: {exc!r}, Update: {update.dict()}")

    try:
        if event.update.callback_query:
            await event.update.callback_query.answer("Произошла ошибка, попробуйте снова", show_alert=True)
        elif event.update.message:
            await event.update.message.answer("Произошла ошибка, попробуйте снова")
    except Exception:
        pass
