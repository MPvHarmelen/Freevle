from . import bp
from .models import Page
from flask import g, render_template, Markup

@bp.context_processor
def inject_sitemap():
    parents = Page.query.filter(Page.parent_id==0)
    return dict(parents=parents)

@bp.route('/')
def home():
    """Show the homepage of the entire website."""
    # TODO: make this work for: Page.parent == None
    return render_template('cms/index.html')

@bp.route('/<page_slug>/')
@bp.route('/<parent_slug>/<page_slug>/')
def page_view(page_slug, parent_slug=None):
    """Show a page from the database."""
    possible_parent_ids = [p.id for p in Page.query.filter(Page.slug == parent_slug).all()] or [0]
    page = Page.query.filter(Page.slug == page_slug).filter(Page.parent_id.in_(possible_parent_ids)).first_or_404()
    page.content = Markup(page.content)
    return render_template('cms/page_view.html', page=page)


# Admin
@bp.route('/create')
@bp.route('/<parent_slug>/create')
@bp.route('/<page_slug>/edit')
@bp.route('/<parent_slug>/<page_slug>/edit')
def page_edit(page_slug=None, parent_slug=None):
    """Create or edit a page."""
    if page_slug is None:
        # First or second routing, create a page.
        ...
    else:
        # Third or fourth routing, edit a page.
        ...

@bp.route('/<page_slug>/delete')
@bp.route('/<parent_slug>/<page_slug>/delete')
def page_delete(page_slug, parent_slug=None):
    """Delete a page."""
    ...