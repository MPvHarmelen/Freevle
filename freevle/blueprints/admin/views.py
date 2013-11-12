from flask import url_for, render_template

from . import bp
from .constants import *

from freevle.blueprints.cms.models import Page, Event
from freevle.blueprints.galleries.models import Album
from freevle.blueprints.news.models import NewsItem

@bp.context_processor
def inject_admin_map():
    for dic in bp.index_views.values():
        if not dic.get('img_url', False):
            dic['img_url'] = url_for(dic['bp_name'] + '.static', filename=dic['img_filename'])
    key = lambda a: a['title']
    return {'admin_map': sorted(bp.index_views.values(), key=key)}

@bp.route('/')
def index():
    """Site wide admin homepage."""
    page_dict = {}
    galleries_dict = {}
    news_dict = {}
    events_dict = {}

    page_dict['recent'] = Page.query.order_by(Page.last_edited.desc()).limit(NUMBER_RECENT_ITEMS)
    galleries_dict['recent'] = Album.query.order_by(Album.last_edited.desc()).limit(NUMBER_RECENT_ITEMS)
    news_dict['recent'] = NewsItem.query.order_by(NewsItem.last_edited.desc()).limit(NUMBER_RECENT_ITEMS)
    events_dict['recent'] = Event.query.order_by(Event.last_edited.desc()).limit(NUMBER_RECENT_ITEMS)

    page_dict['url'] = url_for(bp.index_views['cms_page']['endpoint'])
    # galleries_dict['url'] = url_for(bp.index_views['galleries']['endpoint'])
    # news_items_dict['url'] = url_for(bp.index_views['news']['endpoint'])
    events_dict['url'] = url_for(bp.index_views['cms_event']['endpoint'])

    return render_template('admin/index.html',
                           page_dict=page_dict,
                           galleries_dict=galleries_dict,
                           news_dict=news_dict,
                           events_dict=events_dict,
                           title='Admin | Cygnus Gymnasium'
                           )
