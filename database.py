import sqlite3

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


def create_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(CREATE_BOOKS_TABLE)

    for idx in range(1, 5):
        c.execute(f'INSERT INTO books ( id,name,author,genre, price ) VALUES ( {idx}, "Война и мир", "Толстой Л.Н.","Драма", 23.6 )',
                  [])

    conn.commit()
    conn.close()
