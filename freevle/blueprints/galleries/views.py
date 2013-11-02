from datetime import date

from flask import render_template, Markup
from sqlalchemy import func, extract

from freevle import db
from freevle.utils.functions import imageles_markdown as markdown
from freevle.utils.decorators import paginated_view, archived_view
from . import bp
from .constants import ALBUMS_PER_PAGE
from .models import Album

@paginated_view(ALBUMS_PER_PAGE)
def query_albums_page(album_query):
    return album_query.order_by(Album.date_published.desc())


@bp.route('/')
def overview():
    query = Album.query.filter(Album.date_published <= date.today())
    albums, page, max_page = query_albums_page(query)
    return render_template('galleries/overview.html', albums=albums, page=page,
                            max_page=max_page)

@bp.route('/archief/')
@bp.route('/archief/<int:year>/')
@bp.route('/archief/<int:year>/<int:month>/')
@archived_view('galleries.archive', 'galleries/archive.html')
def archive(year=None, month=None):
    # Return result
    # Filter
    query = Album.query.filter(Album.date_published <= date.today())
    if year is not None:
        query = query.filter(extract('year', Album.date_published) == year)
        if month is not None:
            query = query.filter(extract('month', Album.date_published) == month)
    # Query for albums
    albums, page, max_page = query_albums_page(query)

    # Query for year_list
    oldest_date = db.session.query(Album.date_published).\
                  order_by(Album.date_published.asc()).first()[0]

    albums_in_year = Album.query.\
                     filter(extract('year', Album.date_published) == year).\
                     order_by(Album.date_published.desc())

    return oldest_date, albums_in_year, dict(
        albums=albums,
        page=page,
        max_page=max_page
    )

@bp.route('/<int:year>/<album_slug>/')
def detail(year, album_slug, image_slug=None):
    album = Album.query.filter(extract('year', Album.date_published) == year).\
            filter(Album.slug == album_slug).\
            first_or_404()
    album.description = Markup(markdown(album.description))
    return render_template('galleries/detail.html', album=album)

