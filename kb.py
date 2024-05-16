
from aiogram import types

import texts as tt
from books import Book


# Markups
# /start buttons
def get_markup_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(tt.signIn))
    markup.add(types.KeyboardButton(tt.signUp))
    return markup


def get_markup_signIn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(tt.signIn))
    return markup


def get_markup_books(books: list[Book]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for book in books:
        markup.add(types.InlineKeyboardButton(text=f"{book.Id}. {book.Name}, Автор:{book.Author}, Жанр:{book.Genre}", callback_data=f""))
        markup.add(types.InlineKeyboardButton(text=f"Цена:{book.Price}", callback_data=f""))
    return markup
