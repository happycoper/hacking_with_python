#maybe __import Schreiben

from flask import Flask

app = Flask(__name__)

from Vorlesung.VL2 import routes