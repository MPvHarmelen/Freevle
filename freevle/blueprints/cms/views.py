from . import bp
from .models import Category, Subcategory, Page, PageSection
from flask import render_template, Markup, request
from markdown import Markdown
from ..admin import bp as admin

from freevle import app

markdown = Markdown(output_format='html5', safe_mode='escape').convert

@bp.app_context_processor
def inject_sitemap():
    """Inject categories into context."""
    categories = Category.query.all()
    # TODO: where does 'contact' get in?
    key = lambda a: repr(a)
    rules = sorted(app.url_map.iter_rules(), key=key)
    return dict(categories=categories, url_map=rules)

@bp.app_context_processor
def inject_breadcrumbs():
    """Inject breadcrumbs extracted from url into context."""
    breadcrumbs = request.url.split('/')[1:]
    return dict(breadcrumbs=breadcrumbs)

@bp.route(bp.static_url_path + '/')
@bp.route(bp.static_url_path + '/<path:path>/')
@bp.route(bp.static_url_path + '/<path:path>/<filename>')
@bp.route(bp.static_url_path + '/<path:path>/<filename>.<extension>')
def serve_static(path='', filename='', extension=''):
    file_path = path
    if filename:
        file_path += '/' + filename
    if extension:
        file_path += '.' + extension
    return bp.send_static_file(file_path)


@bp.route('/')
def home():
    """Show the homepage of the entire website."""
    return render_template('cms/index.html')

@bp.route('/<category_slug>/')
def category_view(category_slug):
    """Show an overview of a category, with squares for subcategories."""
    category = Category.query.filter(Category.slug == category_slug).first_or_404()
    return render_template('cms/category_view.html', category=category)

@bp.route('/<category_slug>/<subcategory_slug>/<page_slug>')
def page_view(category_slug, subcategory_slug, page_slug):
    """Show a page from the database."""
    # TODO: find out if this could be put into one query.
    cat = Category.query.filter(Category.slug == category_slug).first_or_404()
    sub = Subcategory.query.filter(Subcategory.category == cat)\
          .filter(Subcategory.slug == subcategory_slug).first_or_404()
    page = Page.query.filter(Page.subcategory == sub)\
           .filter(Page.slug == page_slug).first_or_404()

    for text_section in page.sections.filter(PageSection.section_type == 'text'):
        text_section.content = Markup(markdown(text_section.content))
    return render_template('cms/page_view.html', page=page)


# Admin
# This should change a lot because Floris and Pim want an admin site
@admin.route('/cms/', endpoint='cms_index')
def cms_admin_index():
    """Specific admin index for cms blueprint."""
    return render_template('cms/admin.html')

admin.index_views.append(dict(title="Pagina's", endpoint='cms_index'))

@admin.route('/cms/category/create')
@admin.route('/cms/category/<category_slug>/edit')
def category_edit(category_slug=None):
    """Create or edit a page."""
    if category_slug is None:
        # First routing, create a category.
        ...
    else:

        ...

# admin.add_url_rule('/cms/category/create', 'category_edit', category_edit)
# admin.add_url_rule('/cms/category/<category_slug>/edit', 'category_edit', category_edit)

# @bp.route('/<page_slug>/delete')
# @bp.route('/<parent_slug>/<page_slug>/delete')
def page_delete(page_slug, parent_slug=None):
    """Delete a page."""
    ...
