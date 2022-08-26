import sqlite3


connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    'INSERT INTO person (name, firstname, age) VALUES (?, ?, ?)',
    ('Mustermann', 'Max', 99))

connection.commit()
connection.close()
