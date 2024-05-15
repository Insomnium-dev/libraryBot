from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


# this is a keyboard-buttons file
def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


menu = [
    InlineKeyboardButton("🛒 Каталог", callback_data='catalog'),
    InlineKeyboardButton("💲 Мои заказы", callback_data='orders'),
    InlineKeyboardButton("⚙️ Настройки", callback_data='my_settings'),
    InlineKeyboardButton("❓ Помощь", callback_data='help')
]

catalog = [
    InlineKeyboardButton("Термоэтикетка", callback_data='termoetics'),
    InlineKeyboardButton("Курьерские пакеты", callback_data='packets'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]

orders = [
    InlineKeyboardButton("Текущий заказ", callback_data='current_order'),
    InlineKeyboardButton("История заказов", callback_data='story_orders'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]

settings = [
    InlineKeyboardButton("Мои данные", callback_data='user_data'),
    InlineKeyboardButton("Мои адреса", callback_data='user_addr'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]

help = [
    InlineKeyboardButton("Начать диалог с администратором", callback_data='chat_adm'),
    InlineKeyboardButton("Информация", callback_data='info'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]

termoetics = [
    InlineKeyboardButton("75x120", callback_data='termoetic_75_120'),
    InlineKeyboardButton("58x40", callback_data='termoetic_58_40'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]
packets = [
    InlineKeyboardButton("100x150", callback_data='packets'),
    InlineKeyboardButton("110x210", callback_data='packets'),
    InlineKeyboardButton("150x210", callback_data='packets'),
    InlineKeyboardButton("170x240", callback_data='packets'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]

add_to_basket = [
    InlineKeyboardButton("➖", callback_data='minus'),
    InlineKeyboardButton("0", callback_data='count'),
    InlineKeyboardButton("➕", callback_data='plus'),
    InlineKeyboardButton("◀️ Выйти в меню", callback_data='back')
]

# generate a keyboard
menu_kb = InlineKeyboardMarkup(build_menu(menu, n_cols=2))
catalog_kb = InlineKeyboardMarkup(build_menu(catalog, n_cols=1))
orders_kb = InlineKeyboardMarkup(build_menu(orders, n_cols=1))
settings_kb = InlineKeyboardMarkup(build_menu(settings, n_cols=1))
help_kb = InlineKeyboardMarkup(build_menu(help, n_cols=1))
termoetics_kb = InlineKeyboardMarkup(build_menu(termoetics, n_cols=2))
packets_kb = InlineKeyboardMarkup(build_menu(packets, n_cols=2))
add_to_basket = InlineKeyboardMarkup(build_menu(add_to_basket, n_cols=3))
