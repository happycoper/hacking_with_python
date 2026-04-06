#maybe __import Schreiben

from flask import Flask

app = Flask(__name__)

from . import routes