import sqlite3


conn = sqlite3.connect("data.db")
c = conn.cursor()


class User:
    User_id: int
    Login: str
    Password: str
    def __init__(self, user_id, log, passw):
        self.User_id = user_id
        self.Login = log
        self.Password = passw


def get_user_by_id(value: int):
    c.execute("SELECT * FROM users WHERE user_id=?", [value])
    return User(*(list(c)[0]))

def get_login(value):
    c.execute("SELECT * FROM users WHERE user_id=?", [value])
    return User(*(list(c)[0]))
def set_login(value):
    c.execute(f"UPDATE users SET login=? WHERE user_id=?", [value])
    conn.commit()

def get_password(self):
    return self.__clist()[2]

def set_password(self, value):
    c.execute(f"UPDATE users SET password=? WHERE user_id=?", [value, self.get_id()])
    conn.commit()

def delete_user(value: int):
    c.execute('DELETE FROM users WHERE user_id=?',
              [value])
    conn.commit()



def get_users_list(value):
    c.execute("SELECT * FROM users WHERE user_id!=?",[value])
    return [User(*tmp) for tmp in list(c)]

def create_user(usr: User):
    c.execute(f"INSERT OR REPLACE INTO users ( user_id, login, password) VALUES ( ?, ?, ?)",
                  [usr.User_id, usr.Login, usr.Password])
    conn.commit()
