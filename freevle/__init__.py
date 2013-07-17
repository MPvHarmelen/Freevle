import os
import importlib

from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel
from flask.ext.seasurf import SeaSurf

app = Flask(__name__)
# Load settings (defaults from file, others from wherever user wants)
app.config.from_object('freevle.default_settings')
app.config.from_envvar('FREEVLE_SETTINGS')

# Initialize Flask extensions
db = SQLAlchemy(app)
babel = Babel(app)
csrf = SeaSurf(app)

# Find and import blueprints.
blueprints = os.listdir(app.config['APPS_DIRECTORY'])
for bp_name in blueprints:
    try:
        bp = importlib.import_module('freevle.apps.' + bp_name)
        app.register_blueprint(bp.mod, url_prefix=bp.URL_PREFIX)
    except ImportError:
        raise ImportError("{} app appears to be broken.".format(bp_name))
    except AttributeError:
        raise ImportError("{} app doesn't have mod blueprint.".format(bp_name))
