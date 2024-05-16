import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import message, user
from aiogram.utils.exceptions import MessageNotModified
import kb
import asyncio


import database
import texts as tt
import books

conn = sqlite3.connect("data.db")
c = conn.cursor()

database.create_db()
storage = MemoryStorage()
bot = Bot(token="7049188608:AAHLPVz1skj5OGVuka88VAHwylSqJy6x0pM")
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Добро пожаловать в книжный магазин!\nПожалуйста, авторизуйтесь.",
        reply_markup=kb.get_markup_main(),
    )

@dp.message_handler()
async def handle_text(message):
    if message.text == tt.signIn:
            await bot.send_message(
                chat_id=message.chat.id,
                text=tt.signIn,
                reply_markup=kb.get_markup_signIn(),
            )
    elif message.text == tt.signUp:
            await bot.send_message(
                chat_id=message.chat.id,
                text=tt.signUp,
                reply_markup=kb.get_markup_signUp()
            )
    elif message.text == tt.catalog:
        books_list = books.get_books_list()
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.catalog,
            reply_markup=kb.get_markup_books(books_list)
        )
    else:
        await bot.send_message(message.chat.id, 'Не могу понять команду :(')

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data

    if call_data == "":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=tt.admin_panel,
            reply_markup=kb.get_markup_main(),
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)