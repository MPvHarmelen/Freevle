from flask import Blueprint

bp = Blueprint(
    'virtualcr',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='virtualcr/'
