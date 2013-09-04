import sys, os
import importlib

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel, NullTranslations
from flask.ext.seasurf import SeaSurf

if not hasattr(NullTranslations, 'ugettext'):
    NullTranslations.ugettext = NullTranslations.gettext
if not hasattr(NullTranslations, 'ungettext'):
    NullTranslations.ungettext = NullTranslations.ngettext

app = Flask(__name__)
# Load settings (defaults from file, others from wherever user wants)
app.config.from_object('freevle.default_settings')
if os.environ.get('FREEVLE_SETTINGS', None) is not None:
    app.config.from_envvar('FREEVLE_SETTINGS')
else:
    try:
        app.config.from_pyfile(sys.argv[1])
    except IndexError:
        raise EnvironmentError(("No environment variable set for configuration"
                                " file, nor was an argument given with its"
                                " location."))

# Initialize Flask extensions
db = SQLAlchemy(app)
babel = Babel(app)
csrf = SeaSurf(app)

# Find and import blueprints.
blueprints = os.listdir(app.config['BLUEPRINTS_DIRECTORY'])
for bp_name in blueprints:
    try:
        bp = importlib.import_module('freevle.blueprints.' + bp_name)
        app.register_blueprint(bp.bp, url_prefix=bp.URL_PREFIX)
    except ImportError:
        raise ImportError("{} blueprint appears to be broken.".format(bp_name))
    except AttributeError:
        raise ImportError("{} blueprint doesn't have a blueprint.".format(bp_name))
