import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import message, user
from aiogram.utils.exceptions import MessageNotModified
import kb
import os
import asyncio

import state_handler
import database
import texts as tt
import books
import user as usr


conn = sqlite3.connect("data.db")
c = conn.cursor()


storage = MemoryStorage()
bot = Bot(token="7049188608:AAHLPVz1skj5OGVuka88VAHwylSqJy6x0pM")
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=tt.greet,
        reply_markup=kb.get_markup_main(),
    )


@dp.message_handler()
async def handle_text(message):
    if message.text == tt.signIn:
        # print(message)
        await bot.send_message(
            chat_id=message.chat.id,
            text="Вы зашли как пользователь!\nДля просмотра книг нажмите на кнопку ⬇️",
            reply_markup=kb.get_markup_signIn(),
        )
    elif message.text == tt.signUp:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Вы перешли в окно авторизации!\nНажмите на кнопку \"{tt.admin}\" ⬇️",
            reply_markup=kb.get_markup_adminValidation()
        )

    elif message.text == tt.catalog:
        books_list = books.get_books_list()
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.catalog + ":",
            reply_markup=kb.get_markup_books(books_list)
        )

    elif message.text == tt.registration:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'Вы перешли в окно регистрации. Нажмите на кнопку {tt.registration} ⬇️',
            reply_markup=kb.get_markup_registration()
        )

    else:
        await bot.send_message(message.chat.id, 'Не могу понять команду :(')


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data
    if call_data[:6] == "admin_":
        call_data = call_data[6:]

#// books settings
        if call_data == "booksSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.books,
                reply_markup=kb.get_markup_adminBooksSettings()
            )

        if call_data == "checkBooksList":
            books_list = books.get_books_list()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.catalog + ":",
                reply_markup=kb.get_markup_books(books_list)
            )

        if call_data == "addBookToBooksList":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Введите название книги:",
                reply_markup=kb.single_button(kb.btnBackToAdminSettings)
            )
            await state_handler.addBook.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)

        if call_data == "removeBookFromBooksList":
            books_list = books.get_books_list()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Нажмите на книгу, которую хотите удалить:",
                reply_markup=kb.get_markup_deleteBooks(books_list)
            )

        if call_data.startswith("bookDelete_"):
            book_id = call_data.split('_')[1]
            book = books.get_books_by_id(book_id)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Вы точно хотите удалить эту книгу?",
                reply_markup=kb.get_markup_deleteBook_confirmation(book)
            )

        if call_data.startswith("deleteBook_"):
            book_id = call_data.split('_')[1]
            books.delete_book(book_id)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Книга удалена!",
                reply_markup=kb.get_markup_adminValidation_confirmation()
            )

        if call_data == "editBook":
            books_list = books.get_books_list()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Нажмите на книгу, которую хотите редактировать:",
                reply_markup=kb.get_markup_editBooks(books_list)
            )


        if call_data.startswith("bookEdit_"):
            book_id = call_data.split('_')[1]
            book = books.get_books_by_id(book_id)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Введите название книги:",
                reply_markup=kb.get_markup_startEditBook(book)
            )
            state = Dispatcher.get_current().current_state()
            await state.update_data(id=book_id)
            await state_handler.editBook.name.set()
            await state.update_data(state_message=callback_query.message.message_id)


# // user settings
        if call_data == "usersSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.users,
                reply_markup=kb.get_markup_adminUsersSettings()
            )
    else:
        if call_data == 'backToAdminSettings':
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Меню админа:",
                reply_markup=kb.get_markup_adminValidation_confirmation()
            )

        if call_data.startswith('bookSelected_'):
            book_id = call_data.split('_')[1]
            book = books.get_books_by_id(book_id)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_book_about(book),
                reply_markup=kb.single_button(kb.btnBackBookList),
            )

        if call_data == 'backToBooksList':
            books_list = books.get_books_list()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.catalog + ":",
                reply_markup=kb.get_markup_books(books_list)
            )

        if call_data == 'backToMain':
            await bot.send_message(
                chat_id=chat_id,
                text=tt.greet,
                reply_markup=kb.get_markup_main()
            )

        if call_data == "registration":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Начало регистрации!\nВведите логин:",
                reply_markup=kb.single_button(kb.btnBackToMain)
            )
            await state_handler.registrationData.login.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)

        if call_data == "adminValidation":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Начало авторизации!\nВведите логин:",
                reply_markup=kb.single_button(kb.btnBackToMain)
            )
            await state_handler.adminDataValidation.admLogin.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)





@dp.callback_query_handler(state='*')
async def cancelState(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()

    if call_data == "registrationConfirm":
        await bot.send_message(
            chat_id=chat_id,
            text="Ваши данные успешно сохранены!",
            reply_markup=kb.get_markup_main()
        )
        usr.create_user(usr.User(int(chat_id), data['login'], data['password']))
        await state.finish()

    if call_data == "addBookConfirm":
        await bot.send_message(
            chat_id=chat_id,
            text="Ваши данные успешно сохранены!",
            reply_markup=kb.get_markup_adminValidation_confirmation()
        )
        books.create_book(books.Book(-1, data['name'], data['author'],data['genre'], data['price']))
        await state.finish()

    if call_data == "editBookConfirm":
        await bot.send_message(
            chat_id=chat_id,
            text="Ваши данные успешно сохранены!",
            reply_markup=kb.get_markup_adminValidation_confirmation()
        )
        books.edit_book(books.Book(data['id'], data['name'], data['author'],data['genre'], data['price']))
        await state.finish()


@dp.message_handler(state=state_handler.editBook.name)
async def editBookSetBook(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(name=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите автора книги в формате: Фамилия И.О.",
        reply_markup=kb.single_button(kb.btnBackToAdminSettings)
    )

    await state_handler.editBook.author.set()

@dp.message_handler(state=state_handler.editBook.author)
async def editAuthorSetAuthor(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(author=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите жанр книги:",
        reply_markup=kb.single_button(kb.btnBackToAdminSettings)
    )

    await state_handler.editBook.genre.set()

@dp.message_handler(state=state_handler.editBook.genre)
async def editGenreSetGenre(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(genre=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите цену книги:",
        reply_markup=kb.single_button(kb.btnBackToAdminSettings)
    )

    await state_handler.editBook.price.set()

@dp.message_handler(state=state_handler.editBook.price)
async def editPriceSetPrice(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)

    data = await state.get_data()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text=f"Подтвердите правильность данных: \nНазвание: \"{data['name']}\", \nАвтор: {data['author']}, \nЖанр: {data['genre']}, \nЦена: {data['price']} руб.",
        reply_markup=kb.get_markup_editBook_confirmation()
    )

    await state_handler.editBook.confirmation.set()

@dp.message_handler(state=state_handler.addBook.name)
async def addBookSetBook(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(name=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите автора книги в формате: Фамилия И.О.",
        reply_markup=kb.single_button(kb.btnBackToAdminSettings)
    )

    await state_handler.addBook.author.set()

@dp.message_handler(state=state_handler.addBook.author)
async def addAuthorSetAuthor(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(author=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите жанр книги:",
        reply_markup=kb.single_button(kb.btnBackToAdminSettings)
    )

    await state_handler.addBook.genre.set()

@dp.message_handler(state=state_handler.addBook.genre)
async def addAGenreSetGenre(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(genre=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите цену книги:",
        reply_markup=kb.single_button(kb.btnBackToAdminSettings)
    )

    await state_handler.addBook.price.set()

@dp.message_handler(state=state_handler.addBook.price)
async def addPriceSetPrice(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)

    data = await state.get_data()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text=f"Подтвердите правильность данных: \nНазвание: \"{data['name']}\", \nАвтор: {data['author']}, \nЖанр: {data['genre']}, \nЦена: {data['price']} руб.",
        reply_markup=kb.get_markup_addBook_confirmation()
    )

    await state_handler.addBook.confirmation.set()


@dp.message_handler(state=state_handler.adminDataValidation.admLogin)
async def validateLogin(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    # print(usr.get_user_by_id(user_id).Login)
    # print(usr.get_user_by_id(user_id).Password)
    if message.text == usr.get_user_by_id(user_id).Login:
        await state.update_data(admLogin=message.text)

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["state_message"],
            text="Введите ваш пароль:",
            reply_markup=kb.single_button(kb.btnBackToMain)
        )
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["state_message"],
            text=f"{tt.error}\nЛогин введен неправильно!",
            reply_markup=kb.single_button(kb.btnBackToMain)
        )
        return

    await state_handler.adminDataValidation.admPassword.set()


@dp.message_handler(state=state_handler.adminDataValidation.admPassword)
async def validatePassword(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    if message.text == usr.get_user_by_id(user_id).Password:
        await state.update_data(admLogin=message.text)

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["state_message"],
            text="Вы успешно авторизованы!",
            reply_markup=kb.get_markup_adminValidation_confirmation()
        )
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["state_message"],
            text=f"{tt.error}\nЛогин введен неправильно!",
            reply_markup=kb.single_button(kb.btnBackToMain)
        )
        return

    await state_handler.adminDataValidation.confirmation.set()
    await state.finish()

@dp.message_handler(state=state_handler.registrationData.login)
async def addLoginSetLogin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(message.from_user.id)
    await state.update_data(login=message.text)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text="Введите пароль не менее 6 символов:",
        reply_markup=kb.single_button(kb.btnBackToMain)
    )

    await state_handler.registrationData.password.set()


@dp.message_handler(state=state_handler.registrationData.password)
async def addPasswordSetPassword(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if len(message.text) >= 6:
        await state.update_data(password=message.text)
    else:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["state_message"],
            text=f"{tt.error} \n""Пожалуйста, введите пароль не менее 6 символов:",
            reply_markup=kb.single_button(kb.btnBackToMain)
        )
        return

    data = await state.get_data()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["state_message"],
        text=f"Подтвердите правильность данных: \nЛогин: {data['login']}, \nПароль: {data['password']}",
        reply_markup=kb.get_markup_registrationData_confirmation()
    )

    await state_handler.registrationData.confirmation.set()


if __name__ == '__main__':
    database.create_db()

    executor.start_polling(dp, skip_updates=True)
