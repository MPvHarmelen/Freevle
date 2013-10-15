from freevle import db
from .constants import *

class NewsItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	...

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(EVENT_NAME_LENGTH), nullable=False)
	date = db.Column(db.Date(), nullable=False)
	# link = Same as 'relevant' thing in cms.
