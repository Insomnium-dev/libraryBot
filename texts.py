
greet = "Добро пожаловать в книжный магазин!👋\nПожалуйста, авторизуйтесь."


signIn = "🙋‍♂️ Пользователь"
signUp = "👨‍💻 Админ"
catalog = "📚 Каталог книг"
back = "⬅️ Назад"

def get_book_about(Book):
    return f"""ℹ️ Информация о книге:\n
    Название: "{Book.Name}"
    Автор: {Book.Author}
    Жанр: {Book.Genre}\n
    Цена: {Book.Price} руб."""