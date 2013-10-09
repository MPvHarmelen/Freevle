from . import bp
from .models import User, Group, Permission
from flask import session, request
from flask import render_template, redirect, session, url_for
from .constants import *

@bp.route(LOGIN_URL)
def login(next=LOGIN_URL):
    """
    Log a user in and optionally redirects them back to where they were.
    """
    return render_template('user/login.html', next=next)

@bp.route(LOGIN_URL, methods=['POST'])
def login_post(username=None, password=None, next=LOGIN_URL):
    """
    Log a user in and optionally redirects them back to where they were.
    """
    if session.get('user', None) is None:
        # The user isn't logged in
        if username and password:
            user = User.authenticate(username, password)
            if user is not None:
                # authentication worked
                session.user = user
            else:
                # authentication failed
                return render_template('user/login.html', next=next, failed=True)
        else:
            # Username and/or password were not given
            return render_template('user/login.html', next=next,
                                   no_username=not username,
                                   no_password=not password)
    # The user is logged in
    return redirect(next)

@bp.route('/logout')
def logout(next=None):
    """
    Log a user out and optionally redirects them back to where they were.
    """
    session.user=None
    if next is not None:
        return redirect(next)
    return render_template('user/logout.html')

@bp.route('/<designation>')
def profile_view(designation):
    """View user profile."""

@bp.route('/group/<group_slug>')
def grou_view(group_slug):
    """Overview of a group's members and permissions."""

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
