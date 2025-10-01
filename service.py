import sqlite3
db_connect = sqlite3.connect("library.bd")
def bron(connect, pr, titile , author):
    db_cursor = connect.cursor()
    db_cursor.execute("""SELECT author , title, free FROM books
                      WHERE title == ?, author == ?, free > 0""", (titile , author))
