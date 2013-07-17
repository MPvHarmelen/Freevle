import os
import importlib

from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel
from flask.ext.seasurf import SeaSurf

app = Flask(__name__)
# Load settings (defaults from file, others from wherever user wants)
app.config.from_object('freevle.default_settings')

# Initialize Flask extensions
db = SQLAlchemy(app)
babel = Babel(app)
csrf = SeaSurf(app)

# Find and import blueprints.
blueprints = os.listdir('apps')
for bp_name in blueprints:
    bp = importlib.import_module('apps.' + bp_name)
    app.register_blueprint(bp.bp, url_prefix=bp.URL_PREFIX)
