from aiogram import types

import texts as tt
from books import Book
from user import User

# some buttons
btnBackBookList = types.InlineKeyboardButton(text=tt.back, callback_data="backToBooksList")
btnBackToMain = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, text=tt.back,
                                           callback_data="backToMain")
btnBackToAdminSettings = types.InlineKeyboardButton(text=tt.back, callback_data="backToAdminSettings")
btnBackToAdminBooksSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_booksSettings")
btnBackToAdminUserSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_usersSettings")
def btnConfirmDeleteBook(value): return types.InlineKeyboardButton(text=tt.confirm,
                                                                   callback_data=f"admin_deleteBook_{value}")
def btnConfirmDeleteUser(value): return types.InlineKeyboardButton(text=tt.confirm,
                                                                   callback_data=f"admin_deleteUser_{value}")

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


def get_markup_adminValidation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.admin, callback_data=f"adminValidation"))
    markup.add(btnBackToMain)
    return markup


def get_markup_adminValidation_confirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.books, callback_data=f"admin_booksSettings"))
    markup.add(types.InlineKeyboardButton(text=tt.users, callback_data=f"admin_usersSettings"))
    markup.add(btnBackToMain)
    return markup


def get_markup_adminBooksSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.checkBooks, callback_data=f"admin_checkBooksList"))
    markup.add(types.InlineKeyboardButton(text=tt.addBook, callback_data=f"admin_addBookToBooksList"))
    markup.add(types.InlineKeyboardButton(text=tt.removeBook, callback_data=f"admin_removeBookFromBooksList"))
    markup.add(types.InlineKeyboardButton(text=tt.editBook, callback_data=f"admin_editBook"))
    markup.add(btnBackToAdminSettings)
    return markup


def get_markup_adminUsersSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.checkUsers, callback_data=f"admin_checkUserList"))
    markup.add(types.InlineKeyboardButton(text=tt.addUser, callback_data=f"admin_addUser"))
    markup.add(types.InlineKeyboardButton(text=tt.removeUser, callback_data=f"admin_removeUser"))
    markup.add(btnBackToAdminSettings)
    return markup


def get_markup_books(books: list[Book]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for book in books:
        markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}",
                                              callback_data=f"bookSelected_{book.Id}"))
    markup.add(btnBackToMain)
    return markup

def get_markup_users(users: list[User]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for user in users:
        markup.add(types.InlineKeyboardButton(text=f"[{user.User_id}] - {user.Login}",
                                              callback_data=f"none"))
    markup.add(btnBackToAdminUserSettings)
    return markup

def get_markup_deleteBooks(books: list[Book]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for book in books:
        markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}",
                                              callback_data=f"admin_bookDelete_{book.Id}"))
    markup.add(btnBackToAdminBooksSettings)
    return markup

def get_markup_deleteUsers(users: list[User]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for user in users:
        markup.add(types.InlineKeyboardButton(text=f"[{user.User_id}] - {user.Login}",
                                              callback_data=f"admin_userDelete_{user.User_id}"))
    markup.add(btnBackToAdminUserSettings)
    return markup


def get_markup_editBooks(books: list[Book]):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    for book in books:
        markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}",
                                              callback_data=f"admin_bookEdit_{book.Id}"))
    markup.add(btnBackToAdminBooksSettings)
    return markup

def get_markup_startEditBook(book: Book):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}",
                                          callback_data="none"))
    markup.add(btnBackToAdminBooksSettings)
    return markup

def get_markup_deleteBook_confirmation(book: Book):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text=f"{book.Id}.\"{book.Name}\",\nАвтор:{book.Author}",
                                          callback_data=f"admin_bookDelete_{book.Id}"))
    markup.add(btnConfirmDeleteBook(book.Id))
    markup.add(btnBackToAdminBooksSettings)
    return markup

def get_markup_deleteUser_confirmation(user):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text=f"[{user.User_id}] - {user.Login}",
                                          callback_data=f"admin_userDelete_{user.User_id}"))
    markup.add(btnConfirmDeleteUser(user.User_id))
    markup.add(btnBackToAdminUserSettings)
    return markup

def get_markup_addBook_confirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подтвердить", callback_data=f"addBookConfirm"))
    markup.add(btnBackToAdminBooksSettings)
    return markup

def get_markup_addUser_confirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подтвердить", callback_data=f"addUserConfirm"))
    markup.add(btnBackToAdminUserSettings)
    return markup

def get_markup_editBook_confirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подтвердить", callback_data=f"editBookConfirm"))
    markup.add(btnBackToAdminBooksSettings)
    return markup
def get_markup_registrationData_confirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Подтвердить", callback_data=f"registrationConfirm"))
    markup.add(btnBackToMain)
    return markup
