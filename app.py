import db
import repo
import service

connect = db.connect_db()
curs = connect.cursor()

print("Добавить книгу: 1" \
"Удалить книгу: 2" \
"Добавить читателя: 3" \
"Удалить читателя: 4" \
"Забронировать книгу: 5" \
"Снять бронь: 6" \
"Взять книгу: 7" \
"Сдать книгу: 8" \
"Список взятых читатетелем. книг: 9" \
"Список забронированных читателем книг: 10" \
"Список просроченных книг: 11" \
"Автоматический сброс брони: 12" \
"Поиск книг: 13" \
"" \
"Что вы хотите сделать? Введите номер запроса: ")
to_do= int(input())
if to_do == 1:
    title= input()
    author = input()
    genre = input()
    want_n = input("Вы хотите добавить одну книгу? (введите yes/no) ")
    if want_n == "no":
        n = int(input())
    else:
        n = 1
    
    repo.add_book(connect, title, author, genre, n)




title= input()
author = input()
genre = input()
n = int(input())
full_name = input()
phone = input()
age = int(input())
pr = input()

repo.add_book(connect, title, author, genre, n)
repo.remove_book(connect, title, author)
repo.add_reader(connect, full_name, phone, age)
repo.remove_reader(connect, pr)


service.bron(connect, pr, title, author)
service.remove_bron(connect, pr, title, author)
service.take_book(connect, pr, title, author)
service.back_book(connect, pr, title, author)
