from datetime import date, datetime, timedelta

def bron(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT pr FROM readers
                   WHERE pr = ?""", (pr,))
    reader = cursor.fetchall()
    if not reader:
        return "Читатель не найден"
    cursor.execute("""SELECT id, free FROM books 
                   WHERE title = ? and author = ?""", (title, author))
    book_result = cursor.fetchone()
    if not book_result:
        return "Книга не найдена"
    
    book_id, free = book_result
    
    if free <= 0:
        return "Нет свободных экземпляров книги"
    
    cursor.execute("""SELECT count(*) FROM holds 
                   WHERE pr = ?""", (pr,))
    cnt = cursor.fetchone()[0]
    
    if cnt >= 5:
        return "Превышен лимит броней (максимум 5)"
    today = date.today().strftime("%d/%m/%y")
    
    cursor.execute("""INSERT INTO holds (pr, book_id, date)
                   VALUES (?, ?, ?)""", (pr, book_id, today))
    
    cursor.execute("""UPDATE books 
                   SET free = free - 1 
                   WHERE id = ?""", (book_id,))
    
    connect.commit()
    return "Книга забронирована"
        

def remove_bron(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT pr FROM readers
                   WHERE pr = ?""", (pr,))
    reader = cursor.fetchall()
    if not reader:
        return "Читатель не найден"
    cursor.execute("""SELECT id FROM books
                      WHERE title = ? and author = ?""", (title , author))
    book_result = cursor.fetchone()
    if not book_result:
        return "Книга не найдена"
    book_id = book_result[0]

    cursor.execute("""SELECT pr, book_id FROM holds
                   WHERE pr = ? and id = ?""", (pr, book_id))
    check_bron = cursor.fetchone()
    if not check_bron:
        return "У вас нет брони этой книги"

    cursor.execute("""DELETE FROM holds
                   WHERE pr = ? and book_id = ?""", (pr, book_id))
    cursor.execute("""UPDATE books
                       SET free = free + 1
                       WHERE title = ? and author = ?""", (title, author))
    connect.commit()
    return "Бронь снята"


def take_book(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT free, id FROM books
                   WHERE title = ? and author = ?""", (title , author))
    
    book_result = cursor.fetchone()
    if not book_result:
        return "Книга не найдена"
    
    free, book_id = book_result

    cursor.execute("""SELECT pr, book_id FROM holds
                   WHERE pr = ? and book_id = ?""", (pr, book_id))
    check_bron = cursor.fetchone()

    cursor.execute("""SELECT count(book_id) FROM loans
                   WHERE pr = ?""", (pr,))
    active_takes = cursor.fetchone()[0]

    if active_takes <= 5:
        if free > 0 or check_bron:
            if check_bron:
                cursor.execute("""DELETE FROM holds 
                            WHERE pr = ? and book_id = ?""", (pr, book_id))
            if free > 0:
                cursor.execute("""UPDATE books
                               SET free = free - 1 
                               WHERE id = ?""", (book_id,))
                
            today = date.today().strftime("%d/%m/%y")
            cursor.execute("""INSERT INTO loans(pr, book_id, date)
                           VAlUES (?, ?, ?)""", (pr, book_id, today))
            connect.commit()
            return "Книга выдана"
    return "Нельзя выдать книгу"


def return_book(connect, pr, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id FROM books
                   WHERE title = ? and author = ?""", (title , author))
    
    book_result = cursor.fetchone()
    if not book_result:
        return "Книга не найдена"
    
    book_id = book_result[0]
    
    cursor.execute("""SELECT pr, book_id FROM loans
                   WHERE pr = ? and book_id = ?""", (pr, book_id))
    check_loan = cursor.fetchall()
    if not check_loan:
        return "Вы не брали эту книгу"

    cursor.execute("""DELETE FROM loans
                   WHERE pr = ? and book_id = ?""", (pr, book_id))
    cursor.execute("""UPDATE books
                   SET free = free + 1
                   WHERE id = ?""", (book_id,))
    connect.commit()
    return "Книга возвращена"


def get_taken_books(connect, pr):
    cursor = connect.cursor()
    cursor.execute("""SELECT b.title, b.author, l.date 
                   FROM loans l 
                   JOIN books b ON l.book_id = b.id 
                   WHERE l.pr = ?""", (pr,))
    
    taken_books = []
    for title, author, date_loan_str in cursor.fetchall():
        date_loan = datetime.strptime(date_loan_str, "%d/%m/%y").date()
        date_return = date_loan + timedelta(days=14)
        date_return_str = date_return.strftime("%d/%m/%y")
        taken_books.append((title, author, date_loan_str, date_return_str))
    return taken_books




def get_reserved_books(connect, pr):
    cursor = connect.cursor()
    cursor.execute("""SELECT b.title, b.author, h.date 
                   FROM holds h 
                   JOIN books b ON h.book_id = b.id 
                   WHERE h.pr = ?""", (pr,))
    reserved_books = []
    for title, author, date_reserved_str in cursor.fetchall():
        date_reserved = datetime.strptime(date_reserved_str, "%d/%m/%y").date()
        date_return = date_reserved + timedelta(days=5)
        date_return_str = date_return.strftime("%d/%m/%y")
        reserved_books.append((title, author, date_reserved_str, date_return_str))
    return reserved_books
    

def get_overdue_books(connect):
    cursor = connect.cursor()
    cursor.execute("""SELECT r.pr, r.full_name, b.title, b.author, l.date 
                   FROM loans l 
                   JOIN readers r ON l.pr = r.pr 
                   JOIN books b ON l.book_id = b.id""")
    overdue_books = []
    today = datetime.now().date()
    for pr, title, author, date_loan_str in cursor.fetchall():
        date_loan = datetime.strptime(date_loan_str, "%d/%m/%y").date()
        date_return = date_loan + timedelta(days=14)
        if today > date_loan:
            date_return_str = date_return.strftime("%d/%m/%y")
            overdue_books.append((pr, title, author, date_return_str))
    return overdue_books

    
def auto_remove_reservation(connect):
    cursor = connect.cursor()
    cursor.execute("""SELECT pr, book_id, date FROM holds""")
    cnt = 0
    today = datetime.now().date()
    for pr, book_id, date_reserve_str in cursor.fetchall():
        date_reserve = datetime.strptime(date_reserve_str, "%d/%m/%y").date()
        expiry_date = date_reserve + timedelta(days=5)
        if today > expiry_date:
             cursor.execute("""DELETE FROM holds 
                           WHERE pr = ? AND book_id = ?""", (pr, book_id))
             cnt += 1
    connect.commit()
    return f"Удалено {cnt} броней"

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