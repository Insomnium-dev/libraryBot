import sqlite3


CREATE_BOOKS_TABLE = """
CREATE TABLE IF NOT EXISTS "books"  (
	"id" INTEGER,
	"name" TEXT NOT NULL,
	"author" TEXT NOT NULL,
	"genre" TEXT NOT NULL,
	"price" FLOAT NOT NULL,
	PRIMARY KEY("id")
	)
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS "orders"  (
	"order_id" INTEGER,
	"user_id" INTEGER,
	"item_list" TEXT,
	PRIMARY KEY("order_id")
    )
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS "users"  (
	"user_id" INTEGER NOT NULL,
    "login" TEXT,
    "password" TEXT,
    PRIMARY KEY("user_id")
)
"""


def create_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(CREATE_BOOKS_TABLE)
    c.execute(CREATE_USERS_TABLE)
    c.execute(CREATE_ORDERS_TABLE)

    for idx in range(1, 5):
        c.execute(f'INSERT OR REPLACE INTO books ( id,name,author,genre, price ) VALUES ( {idx}, "Война и мир", "Толстой Л.Н.","Драма", 23.6 )',
                  [])
    c.execute('INSERT OR REPLACE INTO users ( user_id,login,password ) VALUES (1, "login", "password")',[])
    conn.commit()
    conn.close()
