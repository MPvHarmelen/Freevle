from . import bp

@bp.route('/')
def virtualcr_list_view():
    """Show a list of all VirtualCRs."""

@bp.route('/<virtualcr_slug>/')
def virtualcr_view(virtualcr_slug):
    """The overview of a VirtualCR with all its nodes in it."""

# TODO: Think of how these urls should work with sections and nodes and ahhh.
#@bp.route('/<vritual_slug>/<

# Admin
@bp.route('/create')
@bp.route('/<virtualcr_slug>/edit')
def virtualcr_edit(virtualcr_slug=None):
    """Create or edit a VirtualCR"""

@bp.route('/<virtualcr_slug>/delete')
def virtualcr_delete(virtualcr_slug):
    """Delete a VirtualCR."""

#TODO: Route CED view for section and node