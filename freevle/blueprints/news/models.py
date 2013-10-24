from datetime import datetime

from flask import Markup

from freevle import db
from freevle.utils.database import validate_slug
from freevle.utils.decorators import permalink

from .constants import *

class NewsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(NEWS_ITEM_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(NEWS_ITEM_TITLE_LENGTH), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    cover_image_url = db.Column(db.String(NEWS_ITEM_COVER_IMAGE_URL_LENGTH))

    date_published = db.Column(db.Date, nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    validate_slug = db.validates('slug')(validate_slug)

    @permalink
    def get_url(self):
        return 'news.news_item_view', {'slug': self.slug}
