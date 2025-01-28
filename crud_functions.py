import sqlite3

con = sqlite3.connect('products.db')
cursor = con.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS  Products(
ID INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')
for a in range(1, 5):
    cursor.execute('INSERT  INTO Products (title, description, price) VALUES(?, ?, ?)',
                   (f"Продукт: {a}", f"Описание: {a}", f"{a * 100}"))


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    return products


con.commit()
# con.close()