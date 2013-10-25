from . import bp


@bp.route('/nieuws/')
def news_item_overview():
    ...

@bp.route('/nieuws/<int:year>/<int:month>/<int:day>/<slug>')
def news_item_view(year, month, day, slug):
    ...
