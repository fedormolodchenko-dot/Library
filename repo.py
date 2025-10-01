import sqlite3


def add_book(connect, title, author, genre, n=1):
    cursor = connect.Cursor()

    cursor.execute("""SELECT free, total FROM books 
                   WHERE title == ?, author == ?""",(title, author))
    s = cursor.fetchall()
    if s != []:
        cursor.execute("""UPDATE books
                       SET free = free + ?, total = total + ?
                       WHERE title == ?, author == ?""", (n, n, title, author))
    else:
        cursor.execute("""INSERT INTO books
                       (total, free)
                       VALUES(?,?)""", (n,n))
    cursor.commit()

