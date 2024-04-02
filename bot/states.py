from aiogram.filters.state import StatesGroup, State

class Poll(StatesGroup):
    respond_to_isu = State()
    respond_to_name_surname = State()
    respond_to_email = State()