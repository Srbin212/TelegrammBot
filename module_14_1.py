import sqlite3

con = sqlite3.connect('not_telegram.db')
cursor = con.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
ID INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email  TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')
for a in range(1, 11):

    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (f"user{a}", f"example{a}@gmail.com", f"{a}0", "1000"))

for x in range(1, 11, 2):
    cursor.execute('UPDATE Users set balance = ? WHERE username = ?', (500, f"user{x}"))

for x in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username=?', (f"user{x}",))

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
users = cursor.fetchall()

for user in users:
    print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс {user[3]}")


con.commit()
con.close()