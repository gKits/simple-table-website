# Simple Table Website

This is a simple website written in Python with Flask that displays a SQL Table

---

## Setup

### Setup Environment

The usage of a Python Virtual Environment is recommended. To do so run:
- `python -m venv .venv`  to create the venv
- `source .venv/bin/activate`  on Linux/Mac or `.venv/Script/Activate` on Windows to activate the venv
    - If you need to deactivate the venv just run `deactivate` in the terminal

`pip install -r requirements.txt` to install all required libraries

### Create SQL Schematics

Create a file named `schema.sql` (or edit the existing one) and add it to the `./sql_schematics/` directory. Create your desired table structure.  
Design ruling of the table that should be displayed:  
- The table has to have a column specifically named `Id` that has to be `UNIQUE`.  
It is recommended to use `Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT` to avoid problems.  
- It is also to recommended to use `DROP TABLE IF EXISTS table`  
to avoid overwriting errors on reprovisioning  
- You may also add rows into your table by adding an insert statement like `INSERT INTO table (*,*,*) VALUES(*,*,*)`  

You can use the example table (also used in the existing `schema.sql`) as a blueprint: 
```
DROP TABLE IF EXISTS Person;
CREATE TABLE Person (
    Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Firstname TEXT NOT NULL,
    Age INTEGER NOT NULL
);

INSERT INTO Person (Name, Firstname, Age)
VALUES("Reeves", "Keanu", 58)
```
### Provision database

Run `python tablewebsite.py database -h` for help.  
The argument options consist of:
- `optional arguments`
    - `-d / --database /path/to/database.db. . . Path to .db file runnning your database | "./db/database.db" by default`
    - `-n / --name [NAME]. . . . . . . . . . . . Name your website | "tableapp" by default`
    - `-p / --port [PORT]. . . . . . . . . . . . Specify the port you want to run the website on | 5000 by default`
    - `-h / --help . . . . . . . . . . . . . . . shows help message`

### Run website
`python tablewebsite.py run [-d /path/to/database.db] [-n [NAME]] [-p [PORT]] table` to run the website.  
The argument options consist of:
- `positional arguments`
    - `table [TABLE] . . . . . . . . . . . . . . Name of the table you want to display`
- `optional arguments`
    - `-d / --database /path/to/database.db. . . Path to .db file runnning your database | "./db/database.db" by default`
    - `-n / --name [NAME]. . . . . . . . . . . . Name your website | "tableapp" by default`
    - `-p / --port [PORT]. . . . . . . . . . . . Specify the port you want to run the website on | 5000 by default`
    - `-h / --help . . . . . . . . . . . . . . . shows help message`

Run `python tablewebsite.py run -h` for help.  

