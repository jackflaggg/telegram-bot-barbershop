from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    phone_number = State()
    reason = State()
