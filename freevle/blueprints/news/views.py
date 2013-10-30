from datetime import date, datetime
from math import ceil
from flask import render_template, request, Markup, redirect, url_for
from werkzeug.exceptions import NotFound
from sqlalchemy import func, extract

from freevle import db, app
from freevle.utils.functions import headles_markdown as markdown
from . import bp
from .constants import NEWS_ITEMS_PER_PAGE
from .models import NewsItem

@bp.context_processor
def inject_breadcrumbs():
    """Inject breadcrumbs extracted from url into context."""
    url_sections = request.url.split('/')[3:-1]\
                   if request.url.split('/')[-1] == ''\
                   or request.url.split('/')[-1][0] == '?'\
                   else request.url.split('/')[3:]

    breadcrumbs = [(url_sections[0], '/' + url_sections[0])] + [
        (crumb, '')
        for i, crumb in enumerate(url_sections[1:-1])
    ]
    if len(url_sections) > 1:
        breadcrumbs.append((url_sections[-1], ''))
    return dict(breadcrumbs=breadcrumbs)

def query_news_page(news_query, return_all_news=False):
    try:
        page = int(request.args.get('page', 1))
    except ValueError as e:
        if not app.config['DEBUG']:
            raise NotFound
        else:
            raise e
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
    all_news = news_query.order_by(NewsItem.date_published.desc())
    news = all_news[
        NEWS_ITEMS_PER_PAGE * page :
        NEWS_ITEMS_PER_PAGE * (page + 1) if page != -1 else None
    ]
    if len(news) == 0:
        raise NotFound
    for news_item in news:
        # Content preview will be at most 350 chars and will end at the end of
        # the last sentence.
        news_item.content = news_item.content[:350].rsplit('.', 1)[0] + '.'
    page += 1
    return (news, page, all_news) if return_all_news else (news, page)

@bp.route('/')
def overview():
    query = NewsItem.query.filter(NewsItem.date_published <= date.today())
    news, page = query_news_page(query)
    max_page = int(ceil(db.session.query(func.count(NewsItem.id)).\
                   filter(NewsItem.date_published <= date.today()).\
                   first()[0] / NEWS_ITEMS_PER_PAGE))
    if page < 0:
        # Make negative lookup positive again
        page += max_page
    # Make 'page' one based again
    return render_template('news/news.html', news=news, page=page,
                           max_page=max_page)

@bp.route('/archief/')
@bp.route('/archief/<int:year>/')
@bp.route('/archief/<int:year>/<int:month>/')
def archive(year=None, month=None):
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
            return redirect(url_for('news.archive', **url_kwargs))

    queries = [NewsItem.query, db.session.query(func.count(NewsItem.id))]
    queries = [q.filter(NewsItem.date_published <= date.today()) for q in queries]
    if year is not None:
        queries = [query.filter(extract('year', NewsItem.date_published) == year) for query in queries]
    if month is not None:
        queries = [query.filter(extract('month', NewsItem.date_published) == month) for query in queries]
    news, page, all_news = query_news_page(queries[0], True)
    max_page = int(ceil(queries[1].first()[0] / NEWS_ITEMS_PER_PAGE))
    oldest_date = db.session.query(NewsItem.date_published).\
                 order_by(NewsItem.date_published.asc()).first()[0]
    min_year = oldest_date.year if oldest_date is not None else date.today().year
    years = range(min_year, date.today().year + 1)

    # Make months list
    month_list = []
    if year:
        news_in_year = NewsItem.query.\
                       filter(extract('year', NewsItem.date_published) == year).\
                       order_by(NewsItem.date_published.desc())\
                       if month\
                       else all_news
        oldest_month = news_in_year[-1].date_published.month
        newest_month = news_in_year[0].date_published.month
        today = date.today()
        this_year = today.year
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
    return render_template('news/news_archive.html',
                           news=news,
                           years=years,
                           month_list=month_list,
                           current_year=year,
                           current_month=str(month),
                           page=page,
                           max_page=max_page)

@bp.route('/<int:year>/<int:month>/<int:day>/<slug>')
def item_view(year, month, day, slug):
    requested_date = datetime.strptime(
        '{}-{}-{}'.format(year, month, day),
        '%Y-%m-%d'
    ).date()
    item = NewsItem.query.filter(NewsItem.slug == slug).filter(
        NewsItem.date_published == requested_date
    ).first_or_404()
    item.content = Markup(markdown(item.content))
    return render_template('news/news_message.html', item=item)
