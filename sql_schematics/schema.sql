DROP TABLE IF EXISTS person;

CREATE TABLE person (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Firstname TEXT NOT NULL,
    Age INTEGER NOT NULL
);

INSERT INTO person ('Mustermann', 'Max', 99)