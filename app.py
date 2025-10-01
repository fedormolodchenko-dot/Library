import sqlite3
import db
import repo
connect = db.connect_db()
curs = connect.cursor()
title, author, genre = input()
n = int(input())

repo.add_book(connect, title, author, genre, n)