from . import bp

@bp.route('/')
def importer_list_view():
    '''List of all currently installed importers.'''

@bp.route('/<importer_slug>')
def importer_initiate(importer_slug):
    ...

@bp.route('/<importer_slug>/run')
def importer_run(importer_slug):
    ...
