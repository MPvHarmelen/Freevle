from . import bp
from .models import Category, Subcategory, Page, PageSection
from flask import render_template, Markup, request
from markdown import Markdown

markdown = Markdown(output_format='html5', safe_mode='escape').convert

@bp.context_processor
def inject_sitemap():
    """Inject categories into context."""
    categories = Category.query.all()
    # TODO: where does 'contact' get in?
    return dict(categories=categories)

@bp.context_processor
def inject_breadcrumbs():
    """Inject breadcrumbs extracted from url into context."""
    #request.url
    return dict()

@bp.route('/')
def home():
    """Show the homepage of the entire website."""
    # TODO: make this work for: Page.parent == None
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
def admin_index():
    """Site wide admin homepage."""
    ...

def admin():
    """Specific admin index for cms blueprint."""
    ...


# @bp.route('/create')
# @bp.route('/<parent_slug>/create')
# @bp.route('/<page_slug>/edit')
# @bp.route('/<parent_slug>/<page_slug>/edit')
def page_edit(page_slug=None, parent_slug=None):
    """Create or edit a page."""
    if page_slug is None:
        # First or second routing, create a page.
        ...
    else:

        ...

# @bp.route('/<page_slug>/delete')
# @bp.route('/<parent_slug>/<page_slug>/delete')
def page_delete(page_slug, parent_slug=None):
    """Delete a page."""
    ...
