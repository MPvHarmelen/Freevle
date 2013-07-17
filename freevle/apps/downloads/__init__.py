from flask import Blueprint

bp = Blueprint(
    'downloads',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='downloads/'
