from freevle import db

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title
    # slug
    ...
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
    # title
    # slug
    # album = ...
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
