from aiogram.filters.state import StatesGroup, State

class User_Data(StatesGroup):
    respond_to_isu = State()
    respond_to_name_surname = State()
    respond_to_email = State()

class Poll(StatesGroup):
    respond_to_utility = State()
    respond_to_instruments = State()
    respond_to_inter_problems = State()
    respond_to_org_problems = State()
    respond_to_advice = State()
    respond_to_end_of_poll = State()

