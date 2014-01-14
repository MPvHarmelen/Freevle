from datetime import date

from flask import render_template, Markup
from sqlalchemy import extract

from freevle import db
from freevle.utils.decorators import archived_view
from freevle.utils.functions import imageles_markdown as markdown
from freevle.utils.functions import paginate as _paginate

from . import bp
from .constants import ALBUMS_PER_PAGE, ARCHIVE_URL, BLUEPRINT_TITLE
from .models import Album

paginate = lambda items: _paginate(items, ALBUMS_PER_PAGE)

@bp.route('/')
def overview():
    albums = Album.query.filter(Album.date_published <= date.today()).\
             order_by(Album.date_published.desc()).\
             all()
    albums, page, max_page = paginate(albums)
    return render_template('galleries/overview.html', albums=albums, page=page,
                            max_page=max_page, title=BLUEPRINT_TITLE)

@bp.route('/{}/'.format(ARCHIVE_URL))
@bp.route('/{}/<int:year>/'.format(ARCHIVE_URL))
@bp.route('/{}/<int:year>/<int:month>/'.format(ARCHIVE_URL))
@archived_view('galleries.archive', 'galleries/archive.html'.format(ARCHIVE_URL))
def archive(year=None, month=None):
    # Return result
    # Filter
    query = Album.query.filter(Album.date_published <= date.today())
    if year is not None:
        query = query.filter(extract('year', Album.date_published) == year)
        if month is not None:
            query = query.filter(extract('month', Album.date_published) == month)
    # Query for albums
    albums = query.order_by(Album.date_published.desc()).all()
    albums, page, max_page = paginate(albums)

    # Query for year_list
    oldest_date = db.session.query(Album.date_published).\
                  order_by(Album.date_published.asc()).first()[0]

    albums_in_year = Album.query.\
                     filter(extract('year', Album.date_published) == year).\
                     order_by(Album.date_published.desc())

    title = 'Archief | ' + BLUEPRINT_TITLE
    return oldest_date, albums_in_year, dict(
        albums=albums,
        page=page,
        max_page=max_page,
        title=title
    )

@bp.route('/<int:year>/<album_slug>/')
def detail(year, album_slug, image_slug=None):
    album = Album.query.filter(extract('year', Album.date_published) == year).\
            filter(Album.slug == album_slug).\
            first_or_404()
    album.description = Markup(markdown(album.description))
    title = album.title + ' | ' + BLUEPRINT_TITLE
    return render_template('galleries/detail.html', album=album, title=title)

