
def bron(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id, free FROM books
                      WHERE title == ?, author == ?""", (title , author))
    s = cursor.fetchall()
    book_id = s[0]
    free = s[1]

    cursor.execute("""SELECT count(book_id) FROM holds
                   WHERE pr == ?""", (pr))
    cnt = cursor.fetchall()

    if int(free) > 0 and int(cnt) <= 5:
        date = "d/m/y"
        cursor.execute("""INSERT INTO holds (pr, book_id, date)
                       VALUES (?, ?, ?)""", (pr, book_id, date))
        cursor.execute("""UPDATE books
                       SET free = free - 1
                       WHERE title == ?, author == ?""", (title, author))
    cursor.commit()
        
def remove_bron(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id FROM books
                      WHERE title == ?, author == ?""", (title , author))
    book_id = cursor.fetchall()

    cursor.execute("""DELETE FROM holds
                   WHERE pr == ?, book_id == ?""", (pr, book_id))
    cursor.execute("""UPDATE books
                       SET free = free + 1
                       WHERE title == ?, author == ?""", (title, author))
    cursor.commit()

def take_book(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT free, id FROM books
                   WHERE title == ?, author == ?""", (title , author))
    s = cursor.fetchall()
    free = s[0]
    book_id_1 = s[1]
    cursor.execute("""SELECT book_id FROM holds
                   WHERE pr == ?""", (pr))
    book_id_2 = cursor.fetchall()
    cursor.execute("""SELECT count(book_id)
                   WHERE pr == ?""", (pr))
    active_takes = cursor.fetchall()
    if int(active_takes) >= 5:
        if int(free) > 0 or (book_id_1 in book_id_2):
            date = "d/m/y"
            cursor.execute("""UPDATE books
                        SET free = free - 1
                        WHERE title == ?, author == ?""", (title, author))
            cursor.execute("""INSERT INTO loans(pr, book_id, date)
                           VAlUES (?, ?, ?)""", (pr, book_id_1, date))
    cursor.commit()

def back_book(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT free, id FROM books
                   WHERE title == ?, author == ?""", (title , author))
    book_id = cursor.fetchall()
    cursor.execute("""DELETE FROM loans
                   WHERE pr == ?, book_id == ?""", (pr, book_id))
    cursor.execute("""UPDATE books
                   SET free = free + 1
                   WHERE title == ?, author == ?""", (title, author))
    cursor.commit()

def get_taken_books(connect, pr):
    cursor = connect.cursor()
    cursor.execute("""SELECT b.title, b.author, l.date 
                   FROM loans l 
                   JOIN books b ON l.book_id = b.id 
                   WHERE l.pr = ?""", (pr,))
    books = cursor.fetchall()
    return books

def get_reserved_books(connect, pr):
    cursor = connect.cursor()
    cursor.execute("""SELECT b.title, b.author, h.date 
                   FROM holds h 
                   JOIN books b ON h.book_id = b.id 
                   WHERE h.pr = ?""", (pr,))
    books = cursor.fetchall()
    return books
    
def get_overdue_books(connect):
    cursor = connect.cursor()
    cursor.execute("""SELECT r.pr, r.full_name, b.title, b.author, l.date 
                   FROM loans l 
                   JOIN readers r ON l.pr = r.pr 
                   JOIN books b ON l.book_id = b.id 
                   WHERE date(l.date, '+14 days') < date('now')""")
    overdue_books = cursor.fetchall()
    return overdue_books
    
def auto_remove_reservation(connect):
    cursor = connect.cursor()
    cursor.execute("""DELETE FROM holds 
                   WHERE date(date, '+5 days') < date('now')""")
    connect.commit()
