import sqlite3
from . import app
from flask import render_template, request
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR /"v2.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn =get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS items ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "content TEXT NOT NULL, "
        "created_by TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()



@app.route('/') #decorator
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       theuser = request.form.get('username')
       thepass = request.form.get('password')
       print(f"{theuser}, {thepass}")
   return render_template('login.html')

@app.route('/tickets')
def tickets():
    dbitems = [{"id": 1, "priority": 2, "username": "Mark", "title": "sth broken"},
            {"id": 2, "priority": 1, "username": "Nathalie", "title": "nothing woks"},
            {"id": 3, "priority": 3, "username": "luke", "title": "does not looks good"} ]
    return render_template('tickets.html', items=dbitems)

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
       theuser = request.form.get('username')
       email = request.form.get('email')
       thepass1 = request.form.get('password1')
       thepass2 = request.form.get('password2')
       if thepass1 != thepass2:
           print("Passwörter stimmen nicht überein")

       print(f"\n Username: {theuser},\n Email: {email},\n Passwort1: {thepass1},\n Passwort2: {thepass2} \n")
   return render_template('register.html')

