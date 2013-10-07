from importlib import import_module
from os import listdir
from freevle import app
from . import bp
from ..cms.views import admin_index

admin_index = bp.route('/')(admin_index)
admin_views = {}

for bp_name in listdir(app.config['BLUEPRINTS_DIRECTORY']):
    # Try importing admin views from the blueprint. If we can't, that's okay. :(
    try:
        views = import_module('freevle.blueprints.{}.views'.format(bp_name))
    except ImportError as e:
        if len(e.args) and \
           e.args[0] == "No module named 'freevle.blueprints.{}.views'"\
                        .format(bp_name):
            print("NOTICE: {} blueprint has no views.".format(bp_name))
        else:
            raise e
    else:
        if 'admin' not in dir(views):
            print("NOTICE: {} blueprint has no admin.".format(bp_name))
            continue
        admin_views[bp_name] = [bp.route(bp_name + '/')(views.admin)]
        for attr in (attr[5:] for attr in dir(views) if attr[:6] == 'admin_'):
            if len(attr) > 1 and attr != '_index':
                url = bp_name + attr.replace('_', '/')
                view = getattr(views, 'admin' + attr)
                admin_views[bp_name].append(bp.route(url)(view))
