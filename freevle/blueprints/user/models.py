import re
from freevle import db
from sqlalchemy.ext.hybrid import hybrid_property
from freevle.utils.database import validate_slug
from .constants import *

group_permission = db.Table('group_permission',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'),
              nullable=False),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'),
              nullable=False)
)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(PERMISSION_NAME_LENGTH), unique=True, nullable=False)

    def __repr__(self):
        return '({}) Permission {}'.format(self.id, self.name)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(GROUP_NAME_LENGTH), nullable=False)
    slug = db.Column(db.String(GROUP_SLUG_LENGTH), unique=True, nullable=False)
    permissions = db.relationship(Permission,
                                  secondary=group_permission,
                                  lazy='dynamic',
                                  backref=db.backref('groups', lazy='dynamic'))

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        return '({}) Group {}'.format(self.id, self.name)

# for group in POLYMORPHIC_IDENTITIES:
#     db.session.add(Group(name=group, slug=group))
# db.session.commit()

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), nullable=False)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column('type', db.String(USER_TYPE_LENGTH))
    username = db.Column(db.String(USERNAME_LENGTH), unique=True, nullable=False)
    # TODO: Encryption
    password = db.Column(db.String(PASSWORD_LENGTH))
    first_name = db.Column(db.String(FIRST_NAME_LENGTH), nullable=False)
    surname = db.Column(db.String(SURNAME_LENGTH), nullable=False)
    # TODO: Think of a way to save an avatar.
    # avatar =
    email = db.Column(db.String(EMAIL_LENGTH), nullable=False)
    secondary_email = db.Column(db.String(EMAIL_LENGTH))
    phone_number = db.Column(db.String(PHONE_NUMBER_LENGTH))
    groups = db.relationship(Group,
                             secondary=user_group,
                             lazy='dynamic',
                             backref=db.backref('users', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': __qualname__
    }

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.surname

    @db.validates('email')
    def validate_email(self, key, address):
        split = address.split('@')
        if len(split) == 2 and '.' in split[1]:
            return address
        raise ValueError("Invalid email address.")

    @db.validates('secondary_email')
    def validate_secondary_email(self, key, address):
        split = address.split('@')
        if len(split) == 2 and '.' in split[1]:
            return address
        raise ValueError("Invalid email address.")

    @db.validates('phone_number')
    def validate_phone_number(self, key, number):
        if re.match("^\+?\d+$", number):
            return number
        raise ValueError("Invalid telephone number.")

    @staticmethod
    def authenticate(username, password):
        ...

    def has_permission(self, permission_name):
        perms = session.query(Permission.name).union(
            group.permissions for group in self.groups.all()
        )
        return permission_name in perms.all()

    def __repr__(self):
        return '({}) {} {}'.format(self.id, self.user_type.capitalize(), self.full_name)

    def is_polymorphic_of(self, identity):
        if identity in POLYMORPHIC_IDENTITIES:
            return isinstance(self, eval(identity))
        else:
            raise ValueError("'identity' should be in POLYMORPHIC_IDENTITIES")

class Parent(User):
    __mapper_args__ = {'polymorphic_identity': __qualname__}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Teacher(Parent):
    __mapper_args__ = {'polymorphic_identity': __qualname__}

    id = db.Column(db.Integer, db.ForeignKey('parent.id'), primary_key=True)
    designation = db.Column(db.String(DESIGNATION_LENGTH), unique=True,
                            nullable=False)
    validate_designation = db.validates('designation')(validate_slug)

class Admin(User):
    '''Has all permissions.'''
    __mapper_args__ = {'polymorphic_identity': __qualname__}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

parent_student = db.Table('parent_student',
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.id')),
    db.Column('student.id', db.Integer, db.ForeignKey('student.id'))
)

class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __qualname__,
        'inherit_condition': User.id == id
    }

    designation = db.Column(db.String(DESIGNATION_LENGTH), unique=True,
                            nullable=False)
    year = db.Column(db.Integer, nullable=False)
    parents = db.relationship(Parent,
                             secondary=parent_student,
                             order_by=Parent.id,
                             lazy='dynamic',
                             backref=db.backref('children',
                                                order_by=Parent.full_name,
                                                lazy='dynamic')
    )

    validate_designation = db.validates('designation')(validate_slug)

