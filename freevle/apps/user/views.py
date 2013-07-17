from . import bp

@bp.route('/login')
def login():
    ...

@bp.route('/logout')
def logout():
    ...

@bp.route('/<designation>')
def profile_view(designation):
    ...

@bp.route('/group/<group_slug>')
def group_list_view(group_slug):
    ...

@bp.route('/settings/')
@bp.route('/settings/<page>')
def settings_page(page=None):
    ...

# Admin views
@bp.route('/create')
@bp.route('/<designation>/edit')
def user_edit(designation=None):
    ...

@bp.route('/<designation>/delete')
def user_delete(designation):
    ...

@bp.route('/create')
@bp.route('/<group_slug>/edit')
def group_edit(group_slug=None):
    ...

@bp.route('/<group_slug>/delete')
def group_delete(group_slug):
    ...
