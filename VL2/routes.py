import sqlite3
from . import app
from flask import render_template, request, redirect, url_for, make_response
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR /"v2.db"

def get_db_connection(): # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(): #erstellung der Tabelle, wenn sie noch nicht existiert
    conn =get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "username TEXT UNIQUE NOT NULL, "
        "password TEXT NOT NULL)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS items ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "content TEXT NOT NULL CHECK(LENGTH(content) >= 1024), "
        "priority Integer DEFAULT 2, " 
        "created_by TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()



@app.route('/') #decorator
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        theuser = request.form.get('username')
        thepass = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (theuser,))
        user = cur.fetchone()
        conn.close()

        if user and user["password"] == thepass:
            response = make_response(redirect(url_for('tickets')))
            response.set_cookie('username', theuser)
            return response
        else:
            message = "Login fehlgeschlagen"

    return render_template('login.html', message=message)

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
