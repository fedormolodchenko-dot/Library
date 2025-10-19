import db
import repo
import service

connect = db.connect_db("library.bd")
curs = connect.cursor()

to_do = int(input("Добавить книгу: 1\n"
      "Удалить книгу: 2\n"
      "Добавить читателя: 3\n"
      "Удалить читателя: 4\n"
      "Забронировать книгу: 5\n"
      "Снять бронь: 6\n"
      "Взять книгу: 7\n"
      "Сдать книгу: 8\n"
      "Список взятых читателем книг: 9\n"
      "Список забронированных читателем книг: 10\n"
      "Список просроченных книг: 11\n"
      "Автоматический сброс брони: 12\n"
      "Поиск книг: 13\n"
      "\n"
      "Что вы хотите сделать? Введите номер запроса: "))

if to_do == 1:
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    genre = input("Введите жанр книги: ")
    want_n = input("Вы хотите добавить одну книгу? (введите yes/no): ")
    if want_n == "no":
        n = int(input("Введите количество книг: "))
    else:
        n = 1
    repo.add_book(connect, title, author, genre, n)
    print("Книга добавлена")

elif to_do == 2:
    title = input("Введите название книги для удаления: ")
    author = input("Введите автора книги для удаления: ")
    print(repo.remove_book(connect, title, author))

elif to_do == 3:
    full_name = input("Введите ФИ читателя: ")
    phone = input("Введите телефон читателя: ")
    age = int(input("Введите возраст читателя: "))
    repo.add_reader(connect, full_name, phone, age)
    print("Читатель добавлен")

elif to_do == 4:
    pr = input("Введите идентификатор читателя для удаления: ")
    print(repo.remove_reader(connect, pr))

elif to_do == 5:
    pr = input("Введите идентификатор читателя: ")
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    print(service.bron(connect, pr, title, author))
        
elif to_do == 6:
    pr = input("Введите идентификатор читателя: ")
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    print(service.remove_bron(connect, pr, title, author))
    

elif to_do == 7:
    pr = input("Введите идентификатор читателя: ")
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    print(service.take_book(connect, pr, title, author))

elif to_do == 8:
    pr = input("Введите идентификатор читателя: ")
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    print(service.return_book(connect, pr, title, author))

elif to_do == 9:
    pr = input("Введите идентификатор читателя: ")
    books = service.get_taken_books(connect, pr)
    print("Взятые книги:", books)

elif to_do == 10:
    pr = input("Введите идентификатор читателя: ")
    books = service.get_reserved_books(connect, pr)
    print("Забронированные книги:", books)

elif to_do == 11:
    books = service.get_overdue_books(connect)
    print("Просроченные книги:", books)

elif to_do == 12:
   print(service.auto_remove_reservation(connect))
    

elif to_do == 13:
    title = input("Введите название книги (или Enter для пропуска): ") or None
    author = input("Введите автора книги (или Enter для пропуска): ") or None
    genre = input("Введите жанр книги (или Enter для пропуска): ") or None
    books = service.search_books(connect, title, author, genre)
    print("Найдены книги:", books)

else:
    print("Неверный номер запроса")
