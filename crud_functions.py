import sqlite3
from itertools import product

products_data = [
    ('Product1', 'Описание: описание 1', 100),
    ('Product2', 'Описание: описание 2', 200),
    ('Product3', 'Описание: описание 3', 300),
    ('Product4', 'Описание: описание 4', 400)
]


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    UNIQUE ("title") ON CONFLICT REPLACE
    )
    ''')

    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products_data)
    #cursor.execute('DELETE FROM Products')
    connection.commit()
    connection.close()

    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email  TEXT NOT NULL,
    age  INTEGER NOT NULL,
    balance  INTEGER NOT NULL DEFAULT 1000
    )
    ''')

    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age)'
                       ' VALUES (?, ?, ?)', (username, email, age))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    exists = cursor.fetchone() is not None
    connection.close()
    return exists


def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products