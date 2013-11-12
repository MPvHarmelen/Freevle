from flask import render_template, Markup, request
from freevle import db

from . import bp
from .models import Event, Page
from ..admin import bp as admin

@admin.route('/cms/page/')
def cms_page_index():
    """Specific admin index for Page."""
    pages = Page.query.order_by(Page.title).all()
    return render_template('admin/cms_page_index.html', pages=pages)

@admin.route('/cms/category/create')
@admin.route('/cms/category/edit/<category_slug>')
def cms_category_edit(category_slug=None):
    """Create or edit a category."""
    if category_slug is None:
        # First routing, create a category.
        ...
    else:
        ...

@admin.route('/cms/page/<category_slug>/<subcategory_slug>/create')
@admin.route('/cms/page/<category_slug>/<subcategory_slug>/<page_slug>/edit')
def cms_page_edit(category_slug, subcategory_slug, page_slug=None):
    """Create or edit a page."""
    if page_slug is None:
        page = Page(title='', content='')
    else:
        page = Page.get_page(category_slug, subcategory_slug, page_slug)
    return render_template('admin/cms_page_edit.html', page=page)

@admin.route('/cms/page/<category_slug>/<subcategory_slug>/create', methods=['POST'])
@admin.route('/cms/page/<category_slug>/<subcategory_slug>/<page_slug>/edit', methods=['POST'])
def cms_page_save(category_slug, subcategory_slug, page_slug=None):
    if page_slug is None:
        page = Page()
    else:
        page = Page.get_page(category_slug, subcategory_slug, page_slug)
    page.title = Markup.escape(request.form['page_title'])
    # page.slug = request.form['slug']
    page.is_published = True if request.form['publish'] == 'on' else False
    page.content = Markup.escape(request.form['page_content'])
    db.session.add(page)
    db.session.commit()
    return render_template('admin/cms_page_edit.html', page=page)

@admin.route('/cms/page/<category_slug>/<subcategory_slug>/<page_slug>/delete')
def cms_page_delete(category_slug, subcategory_slug, parent_slug=None):
    """Delete a page."""
    ...

@admin.route('/binnenkort/')
def cms_event_index():
    """Specific admin index for Event."""
    events = Event.query.order_by(Event.date).all()
    return render_template('admin/cms_event_index.html', events=events)

@admin.route('/voorpagina/')
def cms_homepage_edit():
    """Specific admin page for editing the homepage."""
    img_url = ''
    return render_template('admin/cms_homepage_edit.html', img_url=img_url)

admin.add_index_view("Pagina's", bp.name, 'admin.cms_page_index',
                     'img/admin_page_icon.png', 'cms_page')

admin.add_index_view("Binnenkort", bp.name, 'admin.cms_event_index',
                     'img/admin_event_icon.png', 'cms_event')

admin.add_index_view("Voorpagina", bp.name, 'admin.cms_homepage_edit',
                     'img/admin_homepage_icon.png', 'cms_homepage')


