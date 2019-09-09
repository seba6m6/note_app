from flask import Flask, g, render_template, request, redirect, url_for, current_app
import sqlite3
import os
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Mysuperdupersecretkey'

def connect_to_db():
    print(os.path.join(current_app.root_path, 'note_app.db'))
    sql = sqlite3.connect(os.path.join(current_app.root_path, 'note_app.db'))
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_to_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['note-text']

        db = get_db()
        db.execute('insert into notes (note) values (?)', [name])
        db.commit()
        return redirect(url_for('notes'))

    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def notes():
    db = get_db()
    cur = db.execute('''select note, done, id from notes''')
    results = cur.fetchall()

    return render_template('notes_list.html', results=results)

@app.route('/done/<int:note_id>', methods=['POST', 'GET'])
def done(note_id):
    db = get_db()
    db.execute('''update notes set done = 1 where id = (?)''',
                     [note_id])
    db.commit()
    return redirect(url_for('notes'))



if __name__ == "__main__":
    app.run()