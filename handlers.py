# this is a handlers for buttons file
import kb
import texts
import basket

from bot import bot



@bot.message_handler(commands=['start'])
def main(message):
    bot.reply_to(message, text=texts.greet.format(name=message.from_user.first_name), reply_markup=kb.menu_kb)
    basket.user_name = message.from_user.username


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "catalog":
        bot.send_message(callback.message.chat.id, text="Каталог:", reply_markup=kb.catalog_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "termoetics":
        bot.send_message(callback.message.chat.id, text="Размеры:", reply_markup=kb.termoetics_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "termoetic_75_120":
        bot.send_message(callback.message.chat.id, text="Количество термоэтикеток 75х120:",
                         reply_markup=kb.add_to_basket)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "termoetic_58_40":
        bot.send_message(callback.message.chat.id, text="Количество термоэтикеток 58х40:",
                         reply_markup=kb.add_to_basket)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    if callback.data == 'add_to_basket':
        def add_to_cart(message):
            try:
                command, item, price = message.text.split()
                if message.chat.id not in cart:
                    cart[message.chat.id] = {}
                cart[message.chat.id][item] = float(price)
                bot.reply_to(message, f"Товар {item} добавлен в корзину. Чтобы посмотреть корзину, напишите /cart")
            except ValueError:
                bot.reply_to(message, "Используйте команду в формате /add <название товара> <цена>")

        @bot.message_handler(commands=['cart'])
        def show_cart(message):
            if message.chat.id in cart and cart[message.chat.id]:
                cart_text = "Товары в корзине:\n"
                total_price = 0
                for item, price in cart[message.chat.id].items():
                    cart_text += f"{item}: {price}\n"
                    total_price += price
                cart_text += f"Итого: {total_price}"
                bot.reply_to(message, cart_text)
            else:
                bot.reply_to(message, "Корзина пуста")

    elif callback.data == "packets":
        bot.send_message(callback.message.chat.id, text="Размеры:", reply_markup=kb.packets_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "orders":
        bot.send_message(callback.message.chat.id, text="Мои заказы:", reply_markup=kb.orders_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "my_settings":
        bot.send_message(callback.message.chat.id, text="Настройки:", reply_markup=kb.settings_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "help":
        bot.send_message(callback.message.chat.id, text="Помощь:", reply_markup=kb.help_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "back":
        bot.send_message(callback.message.chat.id, text="Главное меню:", reply_markup=kb.menu_kb)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)



    else:
        bot.reply_to(callback.message, text="На такую комманду я не запрограммирован..")


if __name__ == "__main__":
    bot.polling(none_stop=True)
