from flask import Blueprint

bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='/admin'

from . import views
