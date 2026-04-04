from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return "hello_page"

@app.route('/home')
def hello_world():
    return "<h1>Hello World</h1><p>this is my page</p>"

@app.route('/welcome')
def welcome():
    mydict = {}
    mydict["username"] = "De"
    mydict["message"] = "this is my massage"

    return render_template("welcome.html", vars=mydict)

@app.route('/actors')
def actors():
    mylist = ["first", "second", "third"]
    return render_template("actors.html", thelist=mylist)
    
if __name__ == "__main__":
    app.run(debug=True) 

#http://127.0.0.1:5000/
