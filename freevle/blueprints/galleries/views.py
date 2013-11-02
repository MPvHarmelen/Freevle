from datetime import date, datetime
from math import ceil

from flask import render_template, request, Markup, redirect, url_for
from sqlalchemy import func, extract
from werkzeug.exceptions import NotFound

from freevle import db, app
from freevle.utils.functions import imageles_markdown as markdown

from . import bp
from .constants import ALBUMS_PER_PAGE
from .models import Album

def query_albums_page(album_query):
    try:
        page = int(request.args.get('page', 1))
    except ValueError as e:
        if not app.config['DEBUG']:
            raise NotFound
        else:
            raise NotFound(e)
    # if page < 0:
    #     raise NotFound
    if page > 0:
        page -= 1 # Make 'page' zero based

    # list slicing lesson:
    # >>> li = [0,1,2,3,4,5,6,7,8,9]
    # >>> li[-2]
    # 8
    # >>> li[-2:0]
    # []
    # >>> li[-2:]
    # [8, 9]
    # >>> li[-2:None]
    # [8, 9]
    # Those last two results are what we're looking for.
    # That's why the if statement is in there.
    all_albums = album_query.order_by(Album.date_published.desc())
    max_page = int(ceil(len(all_albums.all()) / ALBUMS_PER_PAGE))
    albums = all_albums[
        ALBUMS_PER_PAGE * page :
        ALBUMS_PER_PAGE * (page + 1) if page != -1 else None
    ]
    if page < 0:
        # Make negative lookup positive again
        page += max_page
    if (max_page != 0 and abs(page) > max_page) or abs(page) > max_page + 1:
        raise NotFound
    # Make 'page' one based again
    page += 1
    return albums, page, max_page

@bp.route('/')
def overview():
    query = Album.query.filter(Album.date_published <= date.today())
    albums, page, max_page = query_albums_page(query)
    return render_template('galleries/overview.html', albums=albums, page=page,
                            max_page=max_page)

@bp.route('/archief/')
@bp.route('/archief/<int:year>/')
@bp.route('/archief/<int:year>/<int:month>/')
def archive(year=None, month=None):
    # Redirect get request
    url_kwargs = {}
    year_arg = request.args.get('year', False)
    if year_arg != False:
        url_kwargs['year'] = year_arg
        month_arg = request.args.get('month', False)
        if month_arg != False and year_arg:
            url_kwargs['month'] = month_arg
        try:
            for k,v in url_kwargs.items():
                url_kwargs[k] = int(v) if v is not '' else None
        except ValueError as e:
            if not app.config['DEBUG']:
                raise NotFound
            else:
                raise e
        else:
            return redirect(url_for('galleries.archive', **url_kwargs))

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
    min_year = oldest_date.year if oldest_date is not None else date.today().year
    today = date.today()
    this_year = today.year
    years = range(min_year, this_year + 1)

    # Make months list
    month_list = []
    if year:
        albums_in_year = Album.query.\
                         filter(extract('year', Album.date_published) == year).\
                         order_by(Album.date_published.desc())
        oldest_month = albums_in_year[-1].date_published.month
        newest_month = albums_in_year[0].date_published.month
        this_day = today.day
        for month_delta in range(newest_month - oldest_month):
            temp_date = datetime.strptime(
                '{}-{}-{}'.format(
                    this_year,
                    oldest_month + month_delta,
                    this_day
                ),
                '%Y-%m-%d'
            )
            month_list.append(
                (temp_date.strftime('%m').lstrip('0'), temp_date.strftime('%B'))
            )
    return render_template('galleries/archive.html'
                           ,
                           albums=albums,
                           years=years,
                           month_list=month_list,
                           current_year=year,
                           current_month=str(month),
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

