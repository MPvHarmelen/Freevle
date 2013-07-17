from flask import Blueprint

bp = Blueprint(
    'organizer',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='organizer/'
