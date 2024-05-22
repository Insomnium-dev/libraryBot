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


def get_books_by_id(value: int):
    c.execute("SELECT * FROM books WHERE id=?", [value])
    return Book(*(list(c)[0]))


def delete_book(value: int):
    c.execute('DELETE FROM books WHERE id=?',
              [value])
    conn.commit()

def edit_book(book:Book):
    c.execute(f'UPDATE books SET name=?,author=?,genre=?,price=? WHERE id={book.Id}',
              [book.Name, book.Author, book.Genre, book.Price])
    conn.commit()

def create_book(book: Book):
    c.execute('INSERT INTO books( name,author,genre,price) VALUES ( ?, ?, ? ,? )',
              [book.Name, book.Author, book.Genre, book.Price])
    conn.commit()
