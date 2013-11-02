from datetime import date, datetime
from flask import render_template, request, Markup
from sqlalchemy import func, extract

from freevle import db
from freevle.utils.functions import headles_markdown as markdown
from freevle.utils.decorators import paginated_view, archived_view
from . import bp
from .constants import NEWS_ITEMS_PER_PAGE, NEWS_PREVIEW_LENGTH
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

def process_news(news):
    for news_item in news:
        # Content preview will be at most NEWS_PREVIEW_LENGTH chars and will end
        # at the end of the last sentence.
        news_item.content = news_item.content[:NEWS_PREVIEW_LENGTH].rsplit('.', 1)[0] + '.'
        # The closing </p> is added in the template
        news_item.content = Markup(markdown(news_item.content)[:-4])
    return news

@paginated_view(NEWS_ITEMS_PER_PAGE, extra_function=process_news)
def query_news_page(news_query):
    return news_query.order_by(NewsItem.date_published.desc())

@bp.route('/')
def overview():
    query = NewsItem.query.filter(NewsItem.date_published <= date.today())
    news, page, max_page = query_news_page(query)
    return render_template('news/news.html', news=news, page=page,
                           max_page=max_page)

@bp.route('/archief/')
@bp.route('/archief/<int:year>/')
@bp.route('/archief/<int:year>/<int:month>/')
@archived_view('news.archive', 'news/news_archive.html')
def archive(year=None, month=None):
    query = NewsItem.query.filter(NewsItem.date_published <= date.today())
    if year is not None:
        query = query.filter(extract('year', NewsItem.date_published) == year)
        if month is not None:
            query = query.filter(extract('month', NewsItem.date_published) == month)
    news, page, max_page = query_news_page(query)

    oldest_date = db.session.query(NewsItem.date_published).\
                 order_by(NewsItem.date_published.asc()).first()[0]

    news_in_year = NewsItem.query.\
                   filter(extract('year', NewsItem.date_published) == year).\
                   order_by(NewsItem.date_published.desc())
    return oldest_date, news_in_year, dict(
        news=news,
        page=page,
        max_page=max_page
    )
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
