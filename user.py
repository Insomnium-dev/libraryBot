import sqlite3
import sys
import pathlib

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'data.db'
conn = sqlite3.connect(db_file)
c = conn.cursor()

class User:
    user_id: int
    Login: str
    Password: str
    def __init__(self, user_id, log, passw):
        self.user_id = user_id
        self.Login = log
        self.Password = passw

    def get_id(self):
        return self.user_id

    def __clist(self):
        c.execute(f"SELECT * FROM users WHERE user_id=?", [self.get_id()])
        return list(c)[0]

    def get_login(self):
        return self.__clist()[1]

    def set_login(self, value):
        c.execute(f"UPDATE users SET login=? WHERE user_id=?", [value, self.get_id()])
        conn.commit()

    def get_password(self):
        return self.__clist()[2]

    def set_password(self, value):
        c.execute(f"UPDATE users SET password=? WHERE user_id=?", [value, self.get_id()])
        conn.commit()


def get_user_login(message):
    return message.from_user.username


def get_user_list():
    c.execute("SELECT * FROM users")
    return list(map(User, [user[0] for user in list(c)]))


def create_user(usr: User):
    c.execute(f"INSERT INTO users ( user_id, login, password) VALUES ( ?, ?, ?)",
                  [usr.user_id, usr.Login, usr.Password])
    conn.commit()

