import sqlite3
import time


conn = sqlite3.connect("data.db")
c = conn.cursor()



class Book:
    Id: int
    Name: str
    Author: str
    Genre: str
    Price: float


    def __init__(self, id, name, author, genre, price):
        self.Id = id
        self.Name = name
        self.Author = author
        self.Genre = genre
        self.Price = price

def get_books_list():
    c.execute("SELECT * FROM books", [])
    return [Book(*tmp) for tmp in list(c)]

def get_books_by_id(value:int):
    c.execute("SELECT * FROM books WHERE id=?", [value])
    return Book(*(list(c)[0]))

# def create_book(addr: Address):
#     c.execute('INSERT INTO addresses( address,start_work_tine,end_work_time ) VALUES ( ?, ?, ? )',
#              [addr.Address,
#               time.strftime('%H:%M',addr.StartWork),
#               time.strftime('%H:%M',addr.EndWork) ])
#     conn.commit()