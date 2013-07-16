from flask import Flask, session

app = Flask(__name__)

# Initialize database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# TODO: create magical model imports

# TODO: create magical blueprint imports
