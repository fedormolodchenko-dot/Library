import sqlite3

db_connect = sqlite3.connect("library.bd")
db_cursor = db_connect.cursor()

def add_book():
    db_cursor.execute("""SELECT title, author, total, free FROM books""")
    for item in db_cursor.fetchall():
        if item[0]