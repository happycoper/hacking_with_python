from . import app
from flask import render_template, request

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
    dbitems = [{"id": 1, "priority": 2, "username": "Mark", "titel": "sth broken"},
            {"id": 2, "priority": 1, "username": "Nathalie", "titel": "nothing woks"},
            {"id": 3, "priority": 3, "username": "luke", "titel": "does not looks good"} ]
    return render_template('tickets.html', Item=dbitems)

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
       theuser = request.form.get('username')
       email = request.form.get('email')
       thepass1 = request.form.get('password')
       thepass2 = request.form.get('password')

       print(f"{theuser}, {email}, {thepass1},{thepass2}")
   return render_template('register.html')

