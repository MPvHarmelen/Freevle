from flask import Blueprint

bp = Blueprint(
    'cms',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX=''

from . import views, admin_views
