from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from handlers.start import show_menu
from utils.logger import logger

router = Router()

@router.message(StateFilter(None))
async def no_state(message: types.Message, state: FSMContext):
    logger.info("[NO STATE] fallback")
    await show_menu(message, state)