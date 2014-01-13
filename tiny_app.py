from os import getcwd
from flask import Flask

app = Flask(__name__)

@app.route('/')
def return_cwd():
    return getcwd()
