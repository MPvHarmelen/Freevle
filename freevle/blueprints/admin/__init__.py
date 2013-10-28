from flask import Blueprint

class AdminBlueprint(Blueprint):
    index_views = {}

    def add_index_view(self, title, bp_name, endpoint=None, img_filename='img/admin_icon.png'):
        endpoint = 'admin.{}_index'.format(bp_name) if endpoint is None else endpoint

        self.index_views[bp_name] = dict(
            title=title,
            bp_name=bp_name,
            endpoint=endpoint,
            img_filename=img_filename
        )

bp = AdminBlueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)

URL_PREFIX='/admin'

from . import views
