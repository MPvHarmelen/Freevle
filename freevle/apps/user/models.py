from freevle import db
from sqlalchemy.ext.hybrid import hybrid_property
from freevle.utils.database import validate_slug
import re


DESIGNATION_LENGTH = 32
USER_TYPE_LENGTH = 10

group_permission = db.Table('group_permission',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'),
              nullable=False),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'),
              nullable=False)
)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '({}) Permission {}'.format(self.id, self.name)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    slug = db.Column(db.String(32), unique=True, nullable=False)
    permissions = db.relationship(Permission,
                                  secondary=group_permission,
                                  lazy='dynamic',
                                  backref=db.backref('groups', lazy='dynamic'))

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        return '({}) Group {}'.format(self.id, self.name)

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), nullable=False)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column('type', db.String(USER_TYPE_LENGTH))
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    # TODO: Think of a way to save an avatar.
    # avatar =
    email = db.Column(db.String(255), nullable=False)
    secondary_email = db.Column(db.String(255))
    phone_number = db.Column(db.String(32))
    groups = db.relationship(Group,
                             secondary=user_group,
                             lazy='dynamic',
                             backref=db.backref('users', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
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

    def __repr__(self):
        return '({}) {} {}'.format(self.id, self.user_type.capitalize(), self.full_name)

class Parent(User):
    __tablename__ = 'parent'
    __mapper_args__ = {'polymorphic_identity': 'parent'}

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'inherit_condition': User.id==id
    }

    designation = db.Column(db.String(DESIGNATION_LENGTH), unique=True,
                            nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent = db.relationship(Parent,
                             foreign_keys=[parent_id],
                             backref=db.backref('children',
                                                order_by=Parent.full_name,
                                                lazy='dynamic')
    )

    validate_designation = db.validates('designation')(validate_slug)

class Teacher(User):
    __tablename__ = 'teacher'
    __mapper_args__ = {'polymorphic_identity': 'teacher'}

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    designation = db.Column(db.String(DESIGNATION_LENGTH), unique=True,
                            nullable=False)
    validate_designation = db.validates('designation')(validate_slug)

