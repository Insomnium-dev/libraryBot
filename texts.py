
greet = "Добро пожаловать в книжный магазин!👋\nПожалуйста, авторизуйтесь."


signIn = "🙋‍♂️ Пользователь"
signUp = "👨‍💻 Админ"
registration = "📍 Регистрация"
catalog = "📚 Каталог книг"
back = "⬅️ Назад"
error = "❗️ Произошла ошибка!"
confirm = "✅"
my_orders = "📜 Мои заказы"

#admin
users = "Пользователи"
books = "Книги"
admin = "📍 Авторизация"
checkBooks = "Посмотреть каталог книг"
addBook = "Добавить книгу"
removeBook = "Удалить книгу"
editBook = "Редактировать книгу"
checkUsers = "Посмотреть список авторизованных пользователей"
addUser = "Добавить пользователя"
removeUser = "Удалить пользователя"

def get_book_about(Book):
    return f"""ℹ️ Информация о книге:\n
    Название: "{Book.Name}"
    Автор: {Book.Author}
    Жанр: {Book.Genre}\n
    Цена: {Book.Price} руб."""