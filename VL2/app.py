# main programm
from VL2 import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    

# Starten vom Projekt-Root aus mit:
# python -m VL2.app
# pip install mysql-connector-python
# https://www.apachefriends.org/de/download_success.html
# http://localhost/phpmyadmin

# Hydra: 
# hydra -l admin -P /usr/share/worddlist/rockyou.txt 
# -s 5000 192.168.178.22 http-post-form 
# "/login:username=^USER^&passw=^PASS^:S=302"