import sqlite3
import db
import repo
connect = db.connect_db()
curs = connect.cursor()
title= input()
author = input()
genre = input()
n = int(input())
repo.add_book(connect, title, author, genre, n)
repo.remove_book(connect, title, author)
full_name = input()
phone = input()
age = int(input())
repo.add_reader(connect, full_name, phone, age)
pr = input()
repo.remove_reader(connect, pr)
