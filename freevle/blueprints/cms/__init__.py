from flask import Blueprint

bp = Blueprint(
    'cms',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# TODO: Figure out if this should be '/', '' or None
URL_PREFIX=''

from . import views
