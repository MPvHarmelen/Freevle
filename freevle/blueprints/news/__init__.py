from flask import Blueprint

bp = Blueprint(
    'news',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='/nieuws'

from . import views
