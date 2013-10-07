from . import bp

@bp.route('/')
def importer_list_view():
    """List all currently installed importers."""

@bp.route('/<importer_slug>')
def importer_initiate(importer_slug):
    """
    Initiate an importer.

    This is done as defined in the importer's description file.

    """

@bp.route('/<importer_slug>/run')
def importer_run(importer_slug):
    """AJAX interface for actually running Python code."""
