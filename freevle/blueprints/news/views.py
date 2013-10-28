from flask import render_template, request
from werkzeug.exceptions import NotFound
from sqlalchemy import func

from freevle import db
from . import bp
from .constants import NEWS_ITEMS_PER_PAGE
from .models import NewsItem

@bp.route('/')
def news_item_overview():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        raise NotFound
    if page > 0:
        page -= 1 # Make 'page' zero based
    # if page < 0:
    #     raise NotFound

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
    news = NewsItem.query.order_by(NewsItem.date_published.asc())[
        NEWS_ITEMS_PER_PAGE * page :
        NEWS_ITEMS_PER_PAGE * (page + 1) if page != -1 else None
    ]
    if len(news) == 0:
        raise NotFound
    for news_item in news:
        # Content preview will be at most 350 chars and will end at the end of
        # the last sentence.
        news_item.content = news_item.content[:350].rsplit('.', 1)[0] + '.'
    max_page = int(db.session.query(func.count(NewsItem.id)).first()[0] / NEWS_ITEMS_PER_PAGE)
    if page < 0:
        # Make negative lookup positive again
        page += max_page
    # Make 'page' one based again
    page += 1
    return render_template('news/news.html', news=news, page=page,
                           max_page=max_page)

@bp.route('/<int:year>/<int:month>/<int:day>/<slug>')
def news_item_view(year, month, day, slug):
    ...
