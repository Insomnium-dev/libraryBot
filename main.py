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
import sys
import pathlib

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'data.db'
conn = sqlite3.connect(db_file)
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
        print(message)
        await bot.send_message(
            chat_id=message.chat.id,
            text="Вы зашли как пользователь!\nДля просмотра книг нажмите на кнопку ⬇️",
            reply_markup=kb.get_markup_signIn(),
        )
    elif message.text == tt.signUp:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Введите ваш логин:",
            reply_markup=kb.single_button(kb.btnBackToMain)
        )
        # TODO: Create a state handler and validate the input data
        await state_handler.adminDataValidation.login.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(state_message=message.chat.id)

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
        #TODO: SAVING DATA TO DATABASE
        state = Dispatcher.get_current().current_state()
        data = await state.get_data()
        print(chat_id)
        usr.create_user(usr.User(chat_id, data["login"], data["password"]))

        await bot.send_message(
            chat_id=chat_id,
            text="Данные успешно сохранены!",
            reply_markup=kb.get_markup_main(),
        )

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=data["state_message"],
            text="xcscsdcds",
            reply_markup=kb.get_markup_main(),
        )
        await state.finish()


@dp.message_handler(state=state_handler.registrationData.login)
async def addLoginSetLogin(message: types.Message, state: FSMContext):
    data = await state.get_data()
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
    if not os.path.exists('data.db'):
        database.create_db()

    executor.start_polling(dp, skip_updates=True)
