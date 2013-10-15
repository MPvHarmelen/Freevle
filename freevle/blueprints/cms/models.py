import re
from datetime import datetime

from freevle import db
from freevle.utils.database import validate_slug
from freevle.utils.decorators import permalink

from flask import Markup
from sqlalchemy.ext.hybrid import hybrid_property

from ..user.constants import POLYMORPHIC_IDENTITIES, USER_TYPE_LENGTH
from ..user.models import Admin

from ..news.models import NewsItem

from .constants import *

page_group_view = db.Table('page_group_view',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

page_group_edit = db.Table('page_group_edit',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(CATEGORY_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(CATEGORY_SLUG_LENGTH), nullable=False, unique=True)

    validate_slug = db.validates('slug')(validate_slug)

    @permalink
    def get_url(self):
        return 'cms.category_view', {'category_slug': self.slug}

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(SUBCATEGORY_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(SUBCATEGORY_SLUG_LENGTH), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    user_type_view = db.Column(db.String(USER_TYPE_LENGTH))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('category_id', 'slug'),
    )

    category = db.relationship(
        Category,
        backref=db.backref(
            'subcategories',
            order_by='Subcategory.id',
            lazy='dynamic'
        )
    )

    # groups_view = db.relationship(Group,
    #                          secondary=page_group_view,
    #                          order_by=Group.id,
    #                          lazy='dynamic',
    #                          backref=db.backref('pages_view',
    #                                             order_by='Page.id',
    #                                             lazy='dynamic'))

    validate_slug = db.validates('slug')(validate_slug)

    @db.validates('color')
    def validate_hex_color(self, key, value):
        if re.match('^\#[a-fA-F0-9]{6}$', value):
            return value
        else:
            raise ValueError("This is an invalid color code. It must be a html "
                             "hex color code without alpha e.g. #000000")

    @db.validates('user_type_view')
    def validate_user_type_view(self, key, value):
        if value is not None:
            value = value.lower()
            if value in POLYMORPHIC_IDENTITIES:
                return value
            else:
                raise ValueError("user_type_view has to be one of the POLYMORPHIC_IDENTITIES"
                                 "of the user blueprint.")
        else:
            return value

    def can_view(self, user):
        if isinstance(user, Admin):
            return True
        # elif db.join(user.groups, self.groups_view).all():
        #     return True
        # for group in POLYMORPHIC_IDENTITIES:
        #     if group in self.groups_view.all() and \
        #        isinstance(user, eval(group.capitalize()):
        #         return True
        elif isinstance(user, eval(self.user_type_view.capitalize())):
            return True
        return False

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(PAGE_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(PAGE_SLUG_LENGTH), nullable=False)
    # featured_picture = TODO!!
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('subcategory_id', 'slug'),
    )

    subcategory = db.relationship(
        Subcategory,
        backref=db.backref('pages',
            order_by='Page.id',
            lazy='dynamic'
        )
    )

    # groups_edit = db.relationship(
    #     Group,
    #     secondary=page_group_edit,
    #     order_by=Group.id,
    #     lazy='dynamic',
    #     backref=db.backref('pages_edit',
    #         order_by='Page.id',
    #         lazy='dynamic'
    #     )
    # )

    validate_slug = db.validates('slug')(validate_slug)

    @permalink
    def get_url(self):
        return 'cms.page_view', {'page_slug': self.slug,
                                 'subcategory_slug': self.subcategory.slug,
                                 'category_slug': self.subcategory.category.slug}

    def can_edit(self, user):
        if isinstance(user, Admin):
            return True
        # elif db.join(user.groups, self.groups_edit).all():
        #     return True
        # for group in POLYMORPHIC_IDENTITIES:
        #     if group in self.groups_edit.all() and \
        #        isinstance(user, eval(group.capitalize())):
        #         return True
        return False

    def __repr__(self):
        return '({}) {}/{}/{}'.format(self.id, self.subcategory.category.slug,
                                      self.subcategory.slug, self.slug)

class PageSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_type = db.Column('type', db.String(PAGE_SECTION_TYPE_LENGTH))
    title = db.Column(db.String(PAGE_SECTION_TITLE_LENGTH), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('page_id', 'order'),
    )

    __mapper_args__ = {
        'polymorphic_on': section_type,
        'polymorphic_identity': 'base'
    }

    page = db.relationship(
        Page,
        backref=db.backref(
            'sections',
            order_by='PageSection.order',
            lazy='dynamic'
        )
    )

    def __repr__(self):
        return '({}) {}Section'.format(self.id, self.section_type.capitalize())

class TextSection(PageSection):
    __mapper_args__ = {'polymorphic_identity': 'text'}

    id = db.Column(db.Integer, db.ForeignKey('page_section.id'), primary_key=True)
    content = db.Column(db.Text, nullable=False)

    @db.validates('content')
    def validate_content(self, key, value):
        return Markup.escape(value)

class ImageSection(PageSection):
    __mapper_args__ = {'polymorphic_identity': 'image'}
    id = db.Column(db.Integer, db.ForeignKey('page_section.id'), primary_key=True)
    image_path = db.Column(db.String(IMAGE_SECTION_PATH_LENGTH), nullable=False)

    @db.validates('image_path')
    def validate_image_path(self, key, value):
        return value

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = 
    subcategory_id = 
    category_id = 
    news_item_id = 