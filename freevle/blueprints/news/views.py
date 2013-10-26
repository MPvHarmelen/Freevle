from flask import render_template, request
from werkzeug.exceptions import NotFound

from . import bp
from .constants import NEWS_ITEMS_PER_PAGE
from .models import NewsItem

@bp.route('/')
def news_item_overview():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        raise NotFound
    print('Page: ', page)
    if page > 0:
        page -= 1 # Make 'page' zero based
    # if page < 0:
    #     raise NotFound
    news = NewsItem.query.order_by(NewsItem.date_published.asc())[
        NEWS_ITEMS_PER_PAGE * page : NEWS_ITEMS_PER_PAGE * (page + 1)
    ]
    if len(news) == 0:
        raise NotFound
    for news_item in news:
        # Content preview will be at most 350 chars and will end at the end of
        # the last sentence.
        news_item.content = news_item.content[:350].rsplit('.', 1)[0] + '.'
    if page >= 0:
        page += 1
    return render_template('news/news.html', news=news, page=page)

@bp.route('/<int:year>/<int:month>/<int:day>/<slug>')
def news_item_view(year, month, day, slug):
    ...
