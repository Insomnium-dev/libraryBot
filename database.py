import sqlite3
import sys
import pathlib


CREATE_BOOKS_TABLE = """
CREATE TABLE "books" (
	"id" INTEGER,
	"name" TEXT NOT NULL,
	"author" TEXT NOT NULL,
	"genre" TEXT NOT NULL,
	"price" FLOAT NOT NULL,
	PRIMARY KEY("id")
	)
"""

CREATE_USERS_TABLE = """
CREATE TABLE "users" (
	"user_id" INTEGER NOT NULL,
    "login" TEXT,
    "password" TEXT
)
"""


def create_db():
    script_dir = pathlib.Path(sys.argv[0]).parent
    db_file = script_dir / 'data.db'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute(CREATE_BOOKS_TABLE)
    c.execute(CREATE_USERS_TABLE)

    for idx in range(1, 5):
        c.execute(f'INSERT INTO books ( id,name,author,genre, price ) VALUES ( {idx}, "Война и мир", "Толстой Л.Н.","Драма", 23.6 )',
                  [])

    conn.commit()
    conn.close()
