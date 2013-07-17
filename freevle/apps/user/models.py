from freevle import db
from freevle.utils.database import validate_slug
import re

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    designation = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
#    avatar =
    email = db.Column(db.String(255))
    secondary_email = db.Column(db.String(255))
    phone_number = db.Column(db.String(32))

    groups = db.relationship('Group',
                             secondary=user_group,
                             lazy='dynamic',
                             backref=db.backref('users', lazy='dynamic'))
    __table_args__ = (
        db.UniqueConstraint('username'),
        db.UniqueConstraint('designation')
    )

    validate_slug = db.validates('designation')(validate_slug)

    @db.validates('email')
    @db.validates('secondary_email')
    def validate_email(self, key, address):
        split = address.split('@')
        if len(split) == 2 and '.' in split[1]:
            return address
        raise ValueError("Invalid email address.")

    @db.validates('phone_number')
    def validate_phone_number(self, key, number):
        if re.match("^\+?\d+$", number):
            return number
        raise ValueError("Invalid telephone number.")

    def get_full_name(self):
        return self.first_name + ' ' + self.surname

    def __repr__(self):
        return '({id}) {}'.format(self.id, self.get_full_name())

group_permission = db.Table('group_permission',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    slug = db.Column(db.String(32))
    permissions = db.relationship('Permission',
                                  secondary=group_permission,
                                  lazy='dynamic',
                                  backref=db.backref('groups', lazy='dynamic'))

    __table_args__ = (db.UniqueContraint('slug'))

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        return '({id}) {}'.format(self.id, self.name)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    __table_args__ = (UniqueContraint('name'))

    def __repr__(self):
        return '({id}) {}'.format(self.id, self.name)