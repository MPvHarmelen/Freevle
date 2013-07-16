from freevle import db

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.relationship('Page',
                             backref=db.backref('children', lazy='dynamic'))
    title = db.Column(db.String(32))
    slug = db.Column(db.String(32))
    content = db.Column(db.Text)
    last_edited = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint('parent', 'slug', name='_parent_slug_uc'))

