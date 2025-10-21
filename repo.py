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
    connect.commit()


def remove_book(connect, title, author):
    cursor = connect.cursor()
    
    cursor.execute("""SELECT id FROM books
                   WHERE title = ? and author = ? 
                   AND id NOT IN (SELECT book_id FROM loans WHERE book_id = books.id)
                   AND id NOT IN (SELECT book_id FROM holds WHERE book_id = books.id)""", 
                   (title, author))
    
    s = cursor.fetchone()
    
    if s:
        cursor.execute("""DELETE FROM books WHERE id = ?""", (s[0],))
        connect.commit()
        return "Книга удалена"
    
    cursor.execute("""SELECT id FROM books
                   WHERE title = ? and author = ?""", (title, author))
    if cursor.fetchone():
        return "Нельзя удалить книгу"
    return "Книга не найдена"


def add_reader(connect, full_name, phone, age):
    cursor = connect.cursor()
    parts = full_name.strip().split()
    surname, name = parts[0], parts[1]
    pr = (name[0] + surname[0] + str(len(name)) + str(len(surname)) + phone[len(phone) - 4:])
    cursor.execute("""INSERT INTO readers (pr, full_name, phone, age)
                   VALUES (?, ?, ?, ?)""", (pr, full_name, phone, age))
    connect.commit()


def remove_reader(connect, pr):
    cursor = connect.cursor()
    
    cursor.execute("""SELECT pr FROM readers
                   WHERE pr = ? 
                   AND pr NOT IN (SELECT pr FROM loans WHERE pr = readers.pr)
                   AND pr NOT IN (SELECT pr FROM holds WHERE pr = readers.pr)""", 
                   (pr,))
    
    s = cursor.fetchone()
    
    if s:
        cursor.execute("""DELETE FROM readers WHERE pr = ?""", (s[0],))
        connect.commit()
        return "Читатель удален"
    
    cursor.execute("""SELECT pr FROM readers WHERE pr = ?""", (pr,))
    if cursor.fetchone():
        return "Нельзя удалить читателя"
    return "Читатель не найден"



