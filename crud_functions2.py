import sqlite3

con = sqlite3.connect('products.db')
cursor = con.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
'''),
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
''')


for a in range(1, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES(?, ?, ?)",
                   (f"Продукт: {a}", f"Описание: {a}", f"{a * 100}"))


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    con.commit()
    return products


def add_user(username, email, age):
    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES ('{username}', '{email}', '{age}', 1000)")
    con.commit()


def is_included(username):
    user = cursor.execute(f"SELECT * FROM Users WHERE username = ?", (username,))
    if user.fetchone() is None:
        return True
    else:
        return False

con.commit()
# con.close()