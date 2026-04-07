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

def require_login():
    username = request.cookies.get("username")
    if not username:
        return redirect(url_for('login'))
    return None

def init_db(): #erstellung der Tabelle, wenn sie noch nicht existiert
    conn =get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "username TEXT UNIQUE NOT NULL, "
        "email TEXT NOT NULL, "
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

        if not theuser or not thepass:
            message = "Bitte Username und Passwort ausfüllen"
            return render_template('login.html', message=message)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (theuser,)
        )
        user = cur.fetchone()
        conn.close()

        # Login nur erfolgreich wenn alle Werte i.O.
        if user and user["password"] == thepass:
            response = make_response(redirect(url_for('content')))
            response.set_cookie("username", theuser, max_age=3600, httponly=True)
            return response
        else:
            message = "Login fehlgeschlagen"

    return render_template('login.html', message=message)

@app.route('/tickets')
def tickets():
    guard = require_login()
    if guard:
        return guard
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, priority FROM items ORDER BY id DESC")
    dbitems = cur.fetchall()
    conn.close()
    return render_template('tickets.html', items=dbitems)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        theuser = request.form.get('username')
        email = request.form.get('email')
        thepass1 = request.form.get('password1')
        thepass2 = request.form.get('password2')

        if not theuser:
            message = "Username darf nicht leer sein"
        elif not email:
            message = "Email darf nicht leer sein"
        elif thepass1 != thepass2:
            message = "Passwörter stimmen nicht überein"
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (theuser, email, thepass1)
                )
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                message = "Username existiert bereits"
            finally:
                conn.close()

    return render_template('register.html', message=message)

@app.route('/content')
def content():
    guard = require_login()
    if guard:
        return guard
    
    username = request.cookies.get("username")
    return render_template('content.html', username=username)
               