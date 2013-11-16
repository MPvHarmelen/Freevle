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
# from ..user.decorators import login_required

# Temporary views for demo
@bp.route('/groep8/')
def group_8():
    return render_template('cms/groep8.html')

@bp.route('/contact/')
def contact():
    return render_template('cms/contact.html')

# Error handlers
@bp.app_errorhandler(403)
def page_not_fount(e):
    return render_template('cms/403.html'), 403

@bp.app_errorhandler(404)
def page_not_fount(e):
    return render_template('cms/404.html'), 404

@bp.app_errorhandler(500)
def page_not_fount(e):
    return render_template('cms/500.html'), 500

# Static file serving
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
    # so the extension is hard coded.
    if extension:
        file_path += '.' + extension
    return bp.send_static_file(file_path)

# Context processors
@bp.app_context_processor
def inject_menu():
    """Inject unprotected categories into context."""
    categories = Category.query.filter(Category.security_level == None).all()
    return dict(menu_items=categories)


@bp.app_context_processor
def inject_breadcrumbs():
    """
    Inject breadcrumbs extracted from url into context.

    Returns a list of (name, url) tuples.

    """
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

    # Add link if the url exists, otherwise ''
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
    # The last part of the breadcrumb should never be a url
    if len(url_sections) > 0:
        breadcrumbs.append((url_sections[-1].split('?')[0], ''))
    return dict(breadcrumbs=breadcrumbs)

# Views
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
                  # if c.can_view(session.get('user'))
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
