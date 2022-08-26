import sqlite3
from flask import Flask, render_template, request, redirect, flash


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM person')
    conn.close
    return render_template('index.html', title='Table', data=data)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        firstname = request.form['firstname']
        age = request.form['age']

        if not name or not firstname or not age:
            flash('All Attributes are required')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO person (name, firstname, age) VALUES (?, ?, ?)',
                (name, firstname, int(age))
            )
            conn.commit()
            conn.close()

    return render_template('create.html')


@app.route('/', methods=['PUT'])
def create_record(name: str, firstname: str, age: int):
    pass


@app.route('/<index>', methods=['DELETE'])
def delete_record(index: int):
    pass


@app.route('/', methods=['POST'])
def update_record():
    if request.form.get('add_button'):
        pass
    return redirect(index())


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
