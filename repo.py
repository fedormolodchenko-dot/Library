def add_book(connect, title, author, genre, n = 1):
    cursor = connect.cursor()

    cursor.execute("""SELECT free, total FROM books 
                   WHERE title = ? and author = ?""",(title, author))
    s = cursor.fetchall()

    if s != []:
        cursor.execute("""UPDATE books
                       SET free = free + ?, total = total + ?
                       WHERE title = ? and author = ?""", (n, n, title, author))
    else:
        cursor.execute("""INSERT INTO books
                       (title, author, genre, total, free)
                       VALUES(?, ?, ?, ?,?)""", (title, author, genre, n, n))
    cursor.commit()


def remove_book(connect, title, author):
    cursor = connect.cursor()
    cursor.execute("""SELECT id FROM books
                   WHERE title = ? and author = ?""",(title, author))
    book_id = cursor.fetchall()
    if not book_id:
        return "Книга не найдена"
    
    cursor.execute("""SELECT book_id FROM loans
                   WHERE book_id = ?""",(book_id))
    loans = cursor.fetchall()

    cursor.execute("""SELECT book_id FROM holds
                   WHERE book_id = ?""",(book_id))
    holds = cursor.fetchall()

    if loans == [] and holds == []:
        cursor.execute("""DELETE FROM books
                       WHERE title = ? and author = ?""",(title, author))
        cursor.commit()
        return "Книга удалена"
    cursor.commit()
    return "Нельзя удалить книгу"


def add_reader(connect, full_name, phone, age):
    cursor = connect.cursor()
    surname, name = full_name.split()
    pr = name[0] + surname[0] + str(len(name)) + str(len(surname)) + phone[len(phone) - 4:]
    cursor.execute("""INSERT INTO readers (pr, full_name, phone, age)
                   VALUES (?, ?, ?, ?)""", (pr, full_name, phone, age))
    cursor.commit()


def remove_reader(connect, pr):
    cursor = connect.cursor()
    cursor.execute("""SELECT pr FROM readers
                   WHERE pr = ?""", (pr))
    s = cursor.fetchall()
    if not s:
        return "Читатель не найден"
    
    cursor.execute("""SELECT pr FROM loans""")
    loans = cursor.fetchall()

    cursor.execute("""SELECT pr FROM holds""")
    holds = cursor.fetchall()
    
    if loans == [] and holds == []:
        cursor.execute("""DELETE FROM readers 
                       WHERE pr = ?""", (pr))
        cursor.commit()
        return "Читатель удален"
    cursor.commit()
    return "Нельзя удалить читателя"



