import sqlite3


connection = sqlite3.connect('database.db')

with open('./sql_schematics/schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute(
    'INSERT INTO person (name, firstname, age) VALUES (?, ?, ?)',
    ('Mustermann', 'Max', 99)
)

connection.commit()
connection.close()
