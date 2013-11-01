from datetime import datetime
from warnings import warn

from sqlalchemy import extract, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

from freevle import db
from freevle.utils.database import validate_slug
from freevle.utils.decorators import permalink

from .constants import *

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(ALBUM_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(ALBUM_TITLE_LENGTH), nullable=False)
    author = db.Column(db.String(ALBUM_AUTHOR_LENGTH))
    description = db.Column(db.Text, nullable=False)
    date_published = db.Column(db.Date, nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    _validate_slug = validate_slug
    @db.validates('slug')
    def validate_slug(self, key, value):
        value = self._validate_slug(key, value)
        warn("There's an ugly workaround here.")
        if self.date_published:
            slugs_with_same_year = db.session.query(Album.slug).filter(
                extract('year',  Album.date_published) == self.date_published.year
            ).first()
            if slugs_with_same_year and value in slugs_with_same_year:
                raise IntegrityError(None, None, Exception(
                    "The combination of 'date_published.year' and 'slug' must be "
                    "unique."
                ))
        return value

    @hybrid_property
    def cover_image(self):
        image = self.images.filter(Image.is_cover == True).first()
        return image if image else self.images.first()

    @cover_image.setter
    def cover_image(self, image):
        if not isinstance(image, Image):
            raise TypeError("Only an object op type Image can be a cover_image")
        if not image in self.images:
            raise ValueError("Only an image that's part of an Album can be a "
                             "cover_image")
        # Set other images to not cover image
        db.session.execute(
            update(Image.__table__).\
            where(db.and_(Image.album_id == self.id, Image.is_cover == True)).\
            values(is_cover=False)
        )

        # set this image to cover image
        image.is_cover = True
        db.session.add(image)
        db.session.commit()

    @cover_image.expression
    def cover_image(self):
        return self.images.filter(Image.is_cover == True).limit(1)

    @property
    def cover_image_url(self):
        return self.cover_image.image_url

    @permalink
    def get_url(self):
        return 'galleries.detail', {'year': self.date_published.year,
                                    'album_slug': self.slug}

    def __repr__(self):
        return '<({}) {} Album {}>'.format(self.id, self.date_published.year, self.slug)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(IMAGE_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(IMAGE_TITLE_LENGTH), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    is_cover = db.Column(db.Boolean, default=False)
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

