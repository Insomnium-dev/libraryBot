
from aiogram import types

import texts as tt
from books import Book



# some buttons
btnBackBookList = types.InlineKeyboardButton(text=tt.back, callback_data="backToBooksList")


# some functions
def single_button(btn):
    markup = types.InlineKeyboardMarkup()
    markup.add(btn)
    return markup


# Markups
# /start buttons
def get_markup_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(tt.signIn))
    markup.add(types.KeyboardButton(tt.signUp))
    return markup


def get_markup_signIn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text=tt.catalog))
    return markup


def get_markup_books(books: list[Book]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for book in books:
            markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}", callback_data=f"bookSelected_{book.Id}"))
    return markup
