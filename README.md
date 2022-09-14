# Simple Table Website
This is a simple website written in Python with Flask that displays a SQL Table
---
## Setup

### Initialize SQLite Database

#### 1. Create SQL Schematics  
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
#### 2. Provision databse
Run `python init_db.py` to create the database file

#### 3. Run app  
Run `python app.py`  
The website is run on `localhost:5000`

---
## Requirements
> - Flask

To install requirements move to the repos directory and run:  
`pip install -r requirements.txt`


