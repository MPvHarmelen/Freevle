from flask import Blueprint

bp = Blueprint(
    'galleries',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='/fotos'

# from . import views
