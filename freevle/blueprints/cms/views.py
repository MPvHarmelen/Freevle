from datetime import date

from flask import render_template, Markup, request, session

from freevle import db, app
from freevle.utils.functions import imageles_markdown as markdown
from . import bp
from .constants import NUMBER_OF_EVENTS_ON_HOMEPAGE, NUMBER_OF_NEWS_ITEMS_ON_HOMEPAGE
from .constants import NUMBER_OF_ALBUMS_ON_HOMEPAGE, ALBUM_PREVIEW_LENGTH
from .models import Event, Category, Page
from ..news.models import NewsItem
from ..galleries.models import Album
from ..admin import bp as admin
# from ..user.decorators import login_required


@bp.route(bp.static_url_path + '/')
@bp.route(bp.static_url_path + '/<path:path>/')
@bp.route(bp.static_url_path + '/<path:path>/<filename>')
@bp.route(bp.static_url_path + '/<path:path>/<filename>.<extension>')
def serve_static(path='', filename='', extension=''):
    """
    Serve static files.

    Because this blueprint doesn't have a url-prefix, something breaks in Flask,
    and the serving of static files doesn't work. This function just mimics what
    should already work.

    """
    file_path = path
    if filename:
        file_path += '/' + filename
    # The 'path' filter should accept '.', but somehow I couldn't get it to work
    # so this is the hard coding of the extension.
    if extension:
        file_path += '.' + extension
    return bp.send_static_file(file_path)


@bp.app_context_processor
def inject_menu():
    """Inject unprotected categories into context."""
    categories = Category.query.filter(Category.security_level == None).all()
    return dict(menu_items=categories)


@bp.app_context_processor
def inject_breadcrumbs():
    """Inject breadcrumbs extracted from url into context."""
    # Omit the first three parts of the url, these are 'http', an empty string
    # (resulting from the double slash) and the host name.
    # If the url ends with a slash, eg. the last part of the split is empty,
    # or if the url ends with a get part, eg. the last part of the split starts
    #       with a question mark,
    # then omit the last part of the url
    # else use the whole url
    split = request.url.split('/')
    url_sections = split[3:-1]\
                   if split[-1] == ''\
                   or split[-1][0] == '?'\
                   else split[3:]

    breadcrumbs = [
        (
            crumb,
            '/' + '/'.join(url_sections[:i + 1])\
            if app.bound_map.test('/' + '/'.join(url_sections[:i + 1]))\
            else ''
        )
        for i, crumb in enumerate(
            url_sections[:-1]
        )
    ]
    if len(url_sections) > 0:
        breadcrumbs.append((url_sections[-1], ''))
    return dict(breadcrumbs=breadcrumbs)


@bp.route('/')
def home():
    """Show the homepage of the entire website."""
    today = date.today()
    upcomming = Event.query.filter(Event.date >= today).\
                order_by(Event.date.asc()).limit(NUMBER_OF_EVENTS_ON_HOMEPAGE)
    news_items = NewsItem.query.filter(NewsItem.date_published <= today).\
                 order_by(NewsItem.date_published.desc()).\
                 limit(NUMBER_OF_NEWS_ITEMS_ON_HOMEPAGE)
    albums = Album.query.filter(Album.date_published <= today).\
             order_by(Album.date_published.desc()).\
             limit(NUMBER_OF_ALBUMS_ON_HOMEPAGE)
    for album in albums:
        # Content preview will be at most ALBUM_PREVIEW_LENGTH chars and will
        # end at the end of the last sentence.
        album.description = album.description[:ALBUM_PREVIEW_LENGTH].rsplit('.', 1)[0] + '.'
        album.description = Markup(markdown(album.description))
    return render_template('cms/index.html',
                           upcomming=upcomming,
                           news_items=news_items,
                           albums=albums)


@bp.route('/intern/')
# @login_required
def protected_categories():
    """View all protected categories."""
    categories = Category.query.filter(db.not_(Category.security_level == None)).all()
    categories = [c for c in categories
                  # if isinstance(eval(c.security_level.capitalize()), session.get('user'))
                  ]
    return render_template('cms/category_list.html', categories=categories)


@bp.route('/<category_slug>/')
def category_view(category_slug):
    """Show an overview of a category, with squares for subcategories."""
    category = Category.query.filter(Category.slug == category_slug).\
               filter(Category.security_level == None).\
               first_or_404()
    return render_template('cms/category_view.html', category=category)


@bp.route('/<category_slug>/<subcategory_slug>/<page_slug>')
def page_view(category_slug, subcategory_slug, page_slug):
    """Show a page from the database."""
    page = Page.get_page(None, category_slug, subcategory_slug, page_slug)
    page.content = Markup(markdown(page.content))
    for text_section in page.text_sections:
        text_section.content = Markup(markdown(text_section.content))
    return render_template('cms/page_view.html', page=page)


@bp.route('/intern/<category_slug>/<page_slug>')
# @login_required
def protected_page_view(category_slug, page_slug):
    """Show a page from the database."""
    security_level = session.get('user', 'student')
    page = Page.get_page(security_level, category_slug, None, page_slug)
    page.content = Markup(markdown(page.content))
    for text_section in page.text_sections:
        text_section.content = Markup(markdown(text_section.content))
    return render_template('cms/page_view.html', page=page)



# Admin
# This should change a lot because Floris and Pim want an admin site
@admin.route('/cms/', endpoint='cms_index')
def admin_index():
    """Specific admin index for cms blueprint."""
    pages = Page.query.order_by(Page.title).all()
    return render_template('admin/cms_index.html', pages=pages)

admin.add_index_view("Pagina's", bp.name)

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
