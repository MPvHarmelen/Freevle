from flask import render_template, Markup, request
from werkzeug.exceptions import NotFound

from freevle import db
from freevle.utils.functions import paginate

from . import bp
from .constants import PAGES_PER_ADMIN_PAGE
from .models import Event, Page, Category, Subcategory
from ..admin import bp as admin

@admin.route('/cms/page/')
def cms_page_index():
    """Specific admin index for Page."""
    pages = Page.query
    cat_slug =  request.args.get('category', False)
    if cat_slug:
        pages = pages.filter(
            Page.subcategory.has(
                Subcategory.category.has(
                    Category.slug == cat_slug
                )
            )
        )
    visibility = request.args.getlist('visibility')
    if len(visibility):
        if 'everyone' in visibility:
            i = visibility.index('everyone')
            visibility[i] = None
        if 'studentsparents' in visibility:
            i = visibility.index('studentparent')
            visibility[i:i + 1] = ['student', 'parent']
        filters = [
            Page.subcategory.has(
                Subcategory.category.has(
                    Category.safety_level == level
                )
            )
            for level in visibility
        ]
        pages = pages.filter(db.or_(*filters))
    pages = pages.order_by(Page.title.asc()).all()
    pages, page_nr, max_page_nr = paginate(pages)
    return render_template('admin/cms_page_index.html',
                           pages=pages,
                           page=page_nr,
                           max_page=max_page_nr)

@admin.route('/cms/page/create')
@admin.route('/cms/page/<page_id>/edit')
def cms_page_edit(page_id=None):
    """Create or edit a page."""
    if page_id is None:
        page = Page(title='', content='')
    else:
        page = Page.query.get(page_id)
    if page is not None:
        return render_template('admin/cms_page_edit.html', page=page)
    else:
        raise NotFound

@admin.route('/cms/page/create', methods=['POST'])
@admin.route('/cms/page/<page_id>/edit', methods=['POST'])
def cms_page_save(page_id=None):
    if page_id is None:
        page = Page(title='', content='')
    else:
        page = Page.query.get(page_id)
    page.title = Markup.escape(request.form['page_title'])
    # page.slug = request.form['slug']
    page.is_published = True if request.form['publish'] == 'on' else False
    page.content = Markup.escape(request.form['page_content'])
    db.session.add(page)
    db.session.commit()
    return render_template('admin/cms_page_edit.html', page=page)

@admin.route('/cms/page/<page_id>/delete')
def cms_page_delete(page_id):
    """Delete a page."""
    ...

@admin.route('/cms/category/create')
@admin.route('/cms/category/edit/<category_slug>')
def cms_category_edit(category_slug=None):
    """Create or edit a category."""
    if category_slug is None:
        # First routing, create a category.
        ...
    else:
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


