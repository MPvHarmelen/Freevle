from datetime import datetime
from freevle import db
from freevle.utils.database import validate_slug
from freevle.utils.decorators import permalink
from ..user.models import Group

from .constants import *

page_group = db.Table('page_group',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(PAGE_TITLE_LENGTH), nullable=False)
    slug = db.Column(db.String(PAGE_SLUG_LENGTH), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False, default=0)
    parent = db.relationship('Page',
                             remote_side=[id],
                             backref=db.backref('children',
                                                order_by='Page.id',
                                                lazy='dynamic')
    )
    groups = db.relationship(Group,
                             secondary=page_group,
                             order_by=Group.id,
                             lazy='dynamic',
                             backref=db.backref('pages',
                                                order_by='Page.id',
                                                lazy='dynamic'))
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    last_edited = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('parent_id', 'slug'),
    )

    validate_slug = db.validates('slug')(validate_slug)

    @db.validates('parent_id')
    def validate_parent(self, key, parent_id):
        if parent_id is None:
            parent_id = 0
        elif parent_id != 0:
            parent = Page.query.filter(Page.id == parent_id).first()
            if parent is None:
                raise ValueError("This parent doesn't exist.")
            elif parent.parent is not None:
                raise ValueError("This parent has a parent too.")
        return parent_id

    @permalink
    def get_url(self):
        if self.parent:
            parent_slug = self.parent.slug
        else:
            parent_slug = None
        return 'cms.page_view', {'page_slug': self.slug,
                                 'parent_slug': parent_slug}

    def __repr__(self):
        if self.parent is not None:
            path = self.parent.slug + '/' + self.slug
        else:
            path = self.slug
        return '({}) {}'.format(self.id, path)