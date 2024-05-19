from aiogram import types

import texts as tt
from books import Book

# some buttons
btnBackBookList = types.InlineKeyboardButton(text=tt.back, callback_data="backToBooksList")
btnBackToMain = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, text=tt.back, callback_data="backToMain")


# some functions
def single_button(btn):
    markup = types.InlineKeyboardMarkup()
    markup.add(btn)
    return markup


# Markups
# /start buttons
def get_markup_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(tt.signIn))
    markup.add(types.KeyboardButton(tt.signUp))
    markup.add(types.KeyboardButton(tt.registration))
    return markup


def get_markup_signIn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text=tt.catalog))
    return markup

def get_markup_registration():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.registration, callback_data=f"registration"))
    markup.add(btnBackToMain)
    return markup
def get_markup_books(books: list[Book]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for book in books:
        markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}",
                                              callback_data=f"bookSelected_{book.Id}"))
    markup.add(btnBackToMain)
    return markup


def get_markup_registrationData_confirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подтвердить", callback_data=f"registrationConfirm"))
    markup.add(btnBackToMain)
    return markup