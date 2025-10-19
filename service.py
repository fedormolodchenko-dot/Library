def bron(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id, free FROM books
                      WHERE title = ? and author = ?""", (title , author))
    s = cursor.fetchall()
    
    if not s:
        return "Книга не найдена"
    
    book_id = s[0][0] 
    free = s[0][1]     

    cursor.execute("""SELECT count(book_id) FROM holds
                   WHERE pr = ?""", (pr))
    cnt = cursor.fetchall()

    if int(free) > 0 and int(cnt) <= 5:
        date = "19/10/25"
        cursor.execute("""INSERT INTO holds (pr, book_id, date)
                       VALUES (?, ?, ?)""", (pr, book_id, date))
        cursor.execute("""UPDATE books
                       SET free = free - 1
                       WHERE title = ? and author = ?""", (title, author))
        cursor.commit()
        return "Книга забронирована"
    return "Нельзя забронировать книгу"
        

def remove_bron(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id FROM books
                      WHERE title = ? and author = ?""", (title , author))
    
    s = cursor.fetchall()
    if not s:
        return "Книга не найдена"
    book_id = s[0][0]

    cursor.execute("""SELECT pr, id FROM holds
                   WHERE pr = ? and id = ?""", (pr, book_id))
    x = cursor.fetchall()
    if not x:
        return "У вас нет брони этой книги"

    cursor.execute("""DELETE FROM holds
                   WHERE pr = ? and book_id = ?""", (pr, book_id))
    cursor.execute("""UPDATE books
                       SET free = free + 1
                       WHERE title = ? and author = ?""", (title, author))
    cursor.commit()
    return "Бронь снята"


def take_book(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT free, id FROM books
                   WHERE title = ? and author = ?""", (title , author))
    
    book_result = cursor.fetchall()
    if not book_result:
        return "Книга не найдена"
    
    book_id = book_result[0][0]
    free = book_result[0][1]

    cursor.execute("""SELECT book_id FROM holds
                   WHERE pr = ?""", (pr))
    book_id_2 = cursor.fetchall()
    cursor.execute("""SELECT count(book_id)
                   WHERE pr = ?""", (pr))
    active_takes = cursor.fetchall()
    if int(active_takes) <= 5:
        if int(free) > 0 or (book_id in book_id_2):
            date = "13/10/25"
            cursor.execute("""UPDATE books
                        SET free = free - 1
                        WHERE title = ? and author = ?""", (title, author))
            cursor.execute("""INSERT INTO loans(pr, book_id, date)
                           VAlUES (?, ?, ?)""", (pr, book_id, date))
            cursor.commit()
            return "Книга выдана"
    return "Нельзя выдать книгу"

def return_book(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id FROM books
                   WHERE title = ? and author = ?""", (title , author))
    
    book_id = cursor.fetchall()
    if not book_id:
        return "Книга не найдена"
    
    cursor.execute("""SELECT pr, id FROM holds
                   WHERE pr = ? and id = ?""", (pr, book_id))
    x = cursor.fetchall()
    if not x:
        return "Вы не брали эту книгу"

    cursor.execute("""DELETE FROM loans
                   WHERE pr = ? and book_id = ?""", (pr, book_id))
    cursor.execute("""UPDATE books
                   SET free = free + 1
                   WHERE title = ? and author = ?""", (title, author))
    cursor.commit()
    return "Книга возвращена"


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

def search_books(connect, title = None, author = None, genre = None):
    cursor = connect.cursor()
    quest = "SELECT title, author, genre, total, free FROM books WHERE 1=1"
    paramet = []
    if title:
        quest += " AND LOWER(title) LIKE LOWER(?)"
        paramet.append(f"%{title}%")
    if author:
        quest += " AND LOWER(author) LIKE LOWER(?)"
        paramet.append(f"%{author}%")
    if genre:
        quest += " AND LOWER(genre) LIKE LOWER(?)"
        paramet.append(f"%{genre}%")
    
    cursor.execute(quest, paramet)
    books = cursor.fetchall()
    return books