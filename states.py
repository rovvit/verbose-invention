from aiogram.fsm.state import State, StatesGroup

class AppState(StatesGroup):
    check_subscription = State()
    check_by_email = State()