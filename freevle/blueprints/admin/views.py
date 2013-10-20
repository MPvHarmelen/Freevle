from importlib import import_module
from os import listdir
from freevle import app
from . import bp, URL_PREFIX
from flask import url_for, render_template

@bp.context_processor
def inject_admin_map():
    for dic in bp.index_views:
        if not dic.get('img_url', False):
            dic['img_url'] = url_for(dic['bp_name'] + '.static', filename=dic['img_filename'])
    return dict(admin_map=bp.index_views)

@bp.route('/')
def index():
    """Site wide admin homepage."""
    return render_template('admin/index.html')

bp.add_index_view('Dashboard', bp_name='admin', endpoint='admin.index')

