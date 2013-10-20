from datetime import datetime

from flask import Markup

from freevle import db
from freevle.utils.database import validate_slug

from .constants import *

class NewsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(NEWS_ITEM_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(NEWS_ITEM_TITLE_LENGTH), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # More stuff here but I forgot my to do list at home

    date_published = db.Column(db.Date, nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    validate_slug = db.validates('slug')(validate_slug)

    @db.validates('content')
    def validate_content(self, key, value):
        return Markup.escape(value)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(EVENT_NAME_LENGTH), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    # link = Same as 'relevant' thing in cms.
