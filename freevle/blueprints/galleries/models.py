from datetime import datetime

from freevle import db
from freevle.utils.database import validate_slug

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(ABLUM_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(ABLUM_TITLE_LENGTH), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        return '<({}) Album {}>'.format(self.id, self.slug)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(IMAGE_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(IMAGE_TITLE_LENGTH), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(IMAGE_IMAGE_URL_LENGTH), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('slug', 'album_id'),
        db.UniqueConstraint('order', 'album_id')
    )

    album = db.relationship(
        Album,
        backref=db.backref(
            'images',
            order_by='Image.order',
            lazy='dynamic'
        )
    )

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        return '<({}) Image {} of {}>'.format(self.id, self.slug, self.album)

