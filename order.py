import sqlite3


conn = sqlite3.connect("data.db")
c = conn.cursor()


class Order:
    Order_id: int
    User_id: int
    Item_list: str
    def __init__(self, order_id, user_id, item_lst):
        self.Order_id = order_id
        self.User_id = user_id
        self.Item_list = item_lst


def get_order_by_id(value: int):
    c.execute("SELECT * FROM orders WHERE order_id=?", [value])
    return Order(*(list(c)[0]))

def get_orders_by_user_id(value: int):
    c.execute("SELECT * FROM orders", [value])
    return Order(*(list(c)[0]))


def get_orders(value):
    c.execute(f"SELECT * FROM orders WHERE user_id=?", [value])
    return Order(*(list(c)[0]))

def get_item_list(value):
    c.execute("SELECT item_list FROM orders WHERE user_id=?", [value])
    return Order(*(list(c)[0]))
def set_item_list(value):
    c.execute(f"UPDATE orders SET item_list=? WHERE order_id=?", [value])
    conn.commit()

def delete_user(value: int):
    c.execute('DELETE FROM users WHERE user_id=?',
              [value])
    conn.commit()


def create_order(ord: Order):
    c.execute(f"INSERT OR REPLACE INTO orders ( order_id ,user_id, item_list) VALUES ( ?, ?, ?)",
                  [ord.Order_id, ord.User_id, ord.Item_list])
    conn.commit()
