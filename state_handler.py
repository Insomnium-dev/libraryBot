from aiogram.dispatcher.filters.state import StatesGroup, State


class adminDataValidation(StatesGroup):
    admLogin = State()
    admPassword = State()
    confirmation = State()

class registrationData(StatesGroup):
    login = State()
    password = State()
    confirmation = State()

class addBook(StatesGroup):
    name = State()
    author = State()
    genre = State()
    price = State()
    confirmation = State()

class editBook(StatesGroup):
    id = State()
    name = State()
    author = State()
    genre = State()
    price = State()
    confirmation = State()

class addUser(StatesGroup):
    user_id = State()
    login = State()
    password = State()
    confirmation = State()



