DROP TABLE IF EXISTS Person;

CREATE TABLE Person (
    Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Firstname TEXT NOT NULL,
    Age INTEGER NOT NULL
);

INSERT INTO Person (Name, Firstname, Age)
VALUES("Mustermann", "Max", 99)