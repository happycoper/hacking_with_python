from flask import Flask

app = Flask(__name__)

from . import routes # . hier damit routes auch in app.py gefunden wird
routes.init_db() 