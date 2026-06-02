#pip install requests
import requests
import time
import flask

website = "http://141.87.56.55/content"
session = requests.Session()
session.get(website)
cookie_wert = session.cookies.get("username")
print(cookie_wert)

flask.Markup 
    
