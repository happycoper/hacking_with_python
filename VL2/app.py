# main programm
from VL2 import app

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)
    

# Starten vom Projekt-Root aus mit:
# python -m VL2.app
# pip install mysql-connector-python
# https://www.apachefriends.org/de/download_success.html
# http://localhost/phpmyadmin

# Hydra: 
# hydra -l admin -P /usr/share/worddlist/mini.txt 
# 192.168.178.22 -s 5050 http-post-form 
# "/login:username=^USER^&password=^PASS^:S=302"