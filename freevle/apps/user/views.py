from . import bp

@bp.route('/login')
def login():
    """
    Log a user in and optionally redirects them back to wherethey were.
    """

@bp.route('/logout')
def logout():
    """
    Log a user out and optionally redirects them back to where they were.
    """

@bp.route('/<designation>')
def profile_view(designation):
    """View user profile."""

@bp.route('/group/<group_slug>')
def grou_view(group_slug):
    """Overview of a group’s members and permissions."""

@bp.route('/settings/')
@bp.route('/settings/<page>')
def settings_page(page=None):
    """Access user-specific settings for all apps."""

# Admin views
@bp.route('/create')
@bp.route('/<designation>/edit')
def user_edit(designation=None):
    """Create or edit a user."""

@bp.route('/<designation>/delete')
def user_delete(designation):
    """Delete a user."""

@bp.route('/create')
@bp.route('/<group_slug>/edit')
def group_edit(group_slug=None):
    """Create or edit a group and its permissions."""

@bp.route('/<group_slug>/delete')
def group_delete(group_slug):
    """Delete a group."""
