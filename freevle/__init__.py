import sys, os
from importlib import import_module

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel, NullTranslations
from flask.ext.seasurf import SeaSurf

# Python 3 compatibility
if not hasattr(NullTranslations, 'ugettext'):
    NullTranslations.ugettext = NullTranslations.gettext
if not hasattr(NullTranslations, 'ungettext'):
    NullTranslations.ungettext = NullTranslations.ngettext

app = Flask('freevle')
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
blueprints = (bp for bp in os.listdir(app.config['BLUEPRINTS_DIRECTORY']) if bp != 'admin')
for bp_name in blueprints:
    try:
        bp = import_module('freevle.blueprints.' + bp_name)
        app.register_blueprint(bp.bp, url_prefix=bp.URL_PREFIX)
    except ImportError:
        raise ImportError("{} blueprint appears to be broken.".format(bp_name))
    except AttributeError:
        raise ImportError("{} blueprint doesn't have a blueprint.".format(bp_name))

# Admin needs to be registered as last, so other blueprints can register
# admin urls.
admin = import_module('freevle.blueprints.admin')
app.register_blueprint(admin.bp, url_prefix=admin.URL_PREFIX)

app.bound_map = app.url_map.bind(app.config['SERVER_NAME'])
