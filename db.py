import sqlite3

db_connect = sqlite3.connect("library.bd")
db_cursor = db_connect.cursor()

def create_table():
    db_cursor.execute("""CREATE TABLE readers(
              pr    TEXT PRIMARY KEY,
              full_name TEXT NOT NULL,
              phone TEXT NOT NULL,
              age INTEGER NOT NULL)""")
    db_cursor.execute("""CREATE TABLE books(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      author TEXT NOT NULL,
                      genre TEXT NOT NULL,
                      total INTEGER NOT NULL CHECK(total >= 1),
                      free INTEGER NOT NULL CHECK(free >= 0 and free <= total))""")
    db_cursor.execute("""CREATE TABLE loans(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pr TEXT NOT NULL REFERENCES readers(pr),
                      book_id INTEGER NOT NULL REFERENCES books(id),
                      date TEXT NOT NULL)""")
    db_cursor.execute("""CREATE TABLE holds(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pr TEXT NOT NULL REFERENCES readers(pr),
                      book_id INTEGER NOT NULL REFERENCES books(id),
                      date TEXT NOT NULL)""")
    db_connect.commit()
create_table()

def connect_db(path):
    return sqlite3.connect(path)