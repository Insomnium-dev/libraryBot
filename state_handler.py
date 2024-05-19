from aiogram.dispatcher.filters.state import StatesGroup, State


class adminDataValidation(StatesGroup):
    login = State()
    password = State()
    confirmation = State()

class registrationData(StatesGroup):
    login = State()
    password = State()
    confirmation = State()


