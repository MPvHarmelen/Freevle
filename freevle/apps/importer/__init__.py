from flask import Blueprint

bp = Blueprint(
    'importer',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='/importer'
