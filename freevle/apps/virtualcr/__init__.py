from flask import Blueprint

bp = Blueprint(
    '<name>',
    __name__,
    template_folder='templates',
    static_folder='static'
)
