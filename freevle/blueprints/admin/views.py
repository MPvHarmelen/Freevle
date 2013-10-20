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
    return render_template('admin/index.html')

bp.index_views = [dict(title='Dashboard', endpoint='index')]

@bp.context_processor
def inject_admin_map():
    for dic in bp.index_views:
        if not dic.get('img_filename', False):
            dic.update({'img_filename': 'img/index_icon.png'})
    return dict(admin_map=bp.index_views)

