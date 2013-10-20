from importlib import import_module
from os import listdir
from freevle import app
from . import bp, URL_PREFIX
from flask import url_for, render_template

# admin_views = {}
# for bp_name in listdir(app.config['BLUEPRINTS_DIRECTORY']):
#     # Try importing admin views from the blueprint. If we can't, that's okay. :(
#     try:
#         views = import_module('freevle.blueprints.{}.views'.format(bp_name))
#     except ImportError as e:
#         if len(e.args) and \
#            e.args[0] == "No module named 'freevle.blueprints.{}.views'"\
#                         .format(bp_name):
#             print("NOTICE: {} blueprint has no views.".format(bp_name))
#         else:
#             raise e
#     else:
#         if 'admin' not in dir(views):
#             print("NOTICE: {} blueprint has no admin.".format(bp_name))
#             continue
#         admin_views[bp_name] = {'admin': bp.route(bp_name + '/')(views.admin)}
#         for attr in (attr[5:] for attr in dir(views) if attr[:6] == 'admin_'):
#             if len(attr) > 1:
#                 url = bp_name + attr.replace('_', '/')
#                 view = getattr(views, 'admin' + attr)
#                 admin_views[bp_name]['admin' + attr] = bp.route(url)(view)

@bp.route('/')
def index():
    """Site wide admin homepage."""
    blueprints = ((name, url_for(name + '.admin')) for name, views in sorted(bp.index_views.items()))
    return render_template('admin/index.html', blueprints=blueprints)

bp.index_views = {'Home': index}

@bp.context_processor
def inject_admin_map():
    for x in dir(bp.index_views['Home']):
        print(x)
    return dict(admin_map=bp.index_views.items())

