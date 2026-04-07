import mysql.connector
from . import app
from flask import render_template, request, redirect, url_for, make_response
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_CONFIG = {
"host": "127.0.0.1",
"user": "admin",
"password": "admin",
"database": "db_hwp",
"port": 3306
}

def get_db_connection(): # Verbindung zur Datenbank herstellen
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def require_login():
    username = request.cookies.get("username")
    if not username:
        return redirect(url_for('login'))
    return None

def init_db(): #erstellung der Tabelle, wenn sie noch nicht existiert
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "username VARCHAR(50) NOT NULL UNIQUE, "
    "email VARCHAR(120) NOT NULL, "
    "password VARCHAR(255) NOT NULL)"
    )

    cur.execute(
    "CREATE TABLE IF NOT EXISTS items ("
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "title VARCHAR(200) NOT NULL, "
    "content LONGTEXT NOT NULL, "
    "priority INT DEFAULT 2, "
    "created_by VARCHAR(50) NOT NULL)"
    )

    conn.commit()
    cur.close()
    conn.close()



@app.route('/')
def home():
    logout_message = None
    if request.args.get('logout') == '1':
        logout_message = "Erfolgreich ausgeloggt."
    return render_template('home.html', logout_message=logout_message)


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
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT username, password FROM users WHERE username = %s",
            (theuser,)
        )
        user = cur.fetchone()
        conn.close()

        # Login nur erfolgreich wenn alle Werte i.O.
        if user and user[1] == thepass:
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
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, title, priority, created_by FROM items ORDER BY id DESC")
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
            cur = conn.cursor(dictionary=True)
            try:
                cur.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (theuser, email, thepass1)
                )
                conn.commit()
                return redirect(url_for('login'))
            except mysql.connector.IntegrityError:
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

@app.route('/tickets/<int:item_id>')
def ticket_detail(item_id):
    guard = require_login()
    if guard:
        return guard

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, title, content, priority, created_by FROM items WHERE id = %s",
        (item_id,)
    )
    item = cur.fetchone()
    conn.close()

    if not item:
        return "Eintrag nicht gefunden", 404

    return render_template('ticket_detail.html', item=item)

@app.route('/new-item', methods=['GET', 'POST'])
def new_item():
    guard = require_login()
    if guard:
        return guard

    message = None
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        priority = request.form.get('priority')
        created_by = request.cookies.get("username")

        if not title or not content:
            message = "Titel und Inhalt sind Pflichtfelder"
        elif len(content) < 1024:
            message = "Inhalt muss mindestens 1024 Zeichen haben"
        else:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "INSERT INTO items (title, content, priority, created_by) VALUES (%s, %s, %s, %s)",
                (title, content, int(priority), created_by)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('tickets'))

    return render_template('new_item.html', message=message)


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home', logout='1')))
    response.delete_cookie("username")
    return response
               