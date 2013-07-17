from freevle import db
from freevle.utils.database import validate_slug

page_group = db.Table('page_group',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    slug = db.Column(db.String(32))
    parent = db.relationship('Page',
                             backref=db.backref('children', lazy='dynamic'))
    groups = db.relationship('freevle.apps.user.models.Group',
                             secondary=page_group,
                             backref=db.backref('pages', lazy='dynamic'))
    content = db.Column(db.Text)
    last_edited = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('parent', 'slug'))

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        if self.parent is not None:
            path = self.parent.slug + '/' + self.slug
        else:
            path = self.slug
        return '({id}) {}'.format(self.id, path)
