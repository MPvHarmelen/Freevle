import unittest
from freevle.testing import TestBase
from freevle import db
from sqlalchemy.exc import IntegrityError
from .models import Permission, Group, User, Student, Teacher, Parent

class UserTests(TestBase):
    def create_user(self, username='u', first_name='u', surname='u', email='u@u.co',
                    secondary_email='u@u.co', phone_number='+0123456789'):
        u = User(
            username=username,
            first_name=first_name,
            surname=surname,
            email=email,
            secondary_email=secondary_email,
            phone_number=phone_number
        )
        db.session.add(u)
        db.session.commit()
        return u

    def test_user(self):
        # Nice user who knows what should go where
        u_in = self.create_user()
        u = User.query.get(1)
        self.assertEquals(u.username, u_in.username)
        self.assertEquals(u.first_name, u_in.first_name)
        self.assertEquals(u.surname, u_in.surname)
        #self.assertEquals(u.avatar,,)
        self.assertEquals(u.email, u_in.email)
        self.assertEquals(u.secondary_email, u_in.secondary_email)
        self.assertEquals(u.phone_number, u_in.phone_number)

        # Evil users who should be stopped
        self.assertRaises(IntegrityError, self.create_user, username=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_user, first_name=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_user, surname=None)
        db.session.rollback()
        self.assertRaises(ValueError, setattr, u, 'email', "Not an email address")
        self.assertRaises(ValueError, setattr, u, 'secondary_email', "Not an email address either")
        self.assertRaises(ValueError, setattr, u, 'phone_number', "Not a phone number")

        # cleanup
        db.session.delete(u)
        db.session.commit()

    def create_parent(self, username='p', first_name='p', surname='p', email='p@p.co',
                    secondary_email='p@p.co', phone_number='+0123456789'):
        p = Parent(
            username=username,
            first_name=first_name,
            surname=surname,
            email=email,
            secondary_email=secondary_email,
            phone_number=phone_number
        )
        db.session.add(p)
        db.session.commit()
        return p

    def test_parent(self):
        # Nice parent who knows what should go where
        p_in = self.create_parent()
        p = Parent.query.get(1)
        self.assertEquals(p.username, p_in.username)
        self.assertEquals(p.first_name, p_in.first_name)
        self.assertEquals(p.surname, p_in.surname)
        #self.assertEquals(p.avatar,,)
        self.assertEquals(p.email, p_in.email)
        self.assertEquals(p.secondary_email, p_in.secondary_email)
        self.assertEquals(p.phone_number, p_in.phone_number)

        # Evil parents who should be stopped
        self.assertRaises(IntegrityError, self.create_parent, username=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_parent, first_name=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_parent, surname=None)
        db.session.rollback()
        self.assertRaises(ValueError, setattr, p, 'email', "Not an email address")
        self.assertRaises(ValueError, setattr, p, 'secondary_email', "Not an email address either")
        self.assertRaises(ValueError, setattr, p, 'phone_number', "Not a phone number")

        # cleanup
        db.session.delete(p)
        db.session.commit()

    def create_student(self, username='u', first_name='u', surname='u',
                       email='u@u.co', secondary_email='u@u.co',
                       phone_number='+0123456789', designation='u', grade=1,
                       parent=None):
        s = Student(
            username=username,
            first_name=first_name,
            surname=surname,
            email=email,
            secondary_email=secondary_email,
            phone_number=phone_number,
            designation=designation,
            grade=grade,
            parent=parent
        )
        db.session.add(s)
        db.session.commit()
        return s

    def test_student(self):
        # Nice student who knows what should go where
        parent = self.create_parent(username='parent')
        s_in = self.create_student(parent=parent)
        s2 = self.create_student(parent=parent, username='s2', designation='s2')
        s = Student.query.get(2)
        self.assertEquals(s.first_name, s_in.first_name)
        self.assertEquals(s.surname, s_in.surname)
        #self.assertEquals(s.avatar,,)
        self.assertEquals(s.email, s_in.email)
        self.assertEquals(s.secondary_email, s_in.secondary_email)
        self.assertEquals(s.phone_number, s_in.phone_number)
        self.assertEquals(s.designation, s_in.designation)
        self.assertEquals(s.grade, s_in.grade)
        self.assertEquals(s.parent, s_in.parent)
        self.assertEquals(parent.children.all(), [s_in, s2])

        # Evil students who should be stopped
        self.assertRaises(IntegrityError, self.create_student, username=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_student, first_name=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_student, surname=None)
        db.session.rollback()
        self.assertRaises(ValueError, setattr, s, 'email', "Not an email address")
        self.assertRaises(ValueError, setattr, s, 'secondary_email', "Not an email address either")
        self.assertRaises(ValueError, setattr, s, 'phone_number', "Not a phone number")
        self.assertRaises(ValueError, setattr, s, 'designation', "Not a slug")

        # cleanup
        db.session.delete(s)
        db.session.commit()

    def create_teacher(self, username='u', first_name='u', surname='u',
                       email='u@u.co', secondary_email='u@u.co',
                       phone_number='+0123456789', designation='u'):
        t = Teacher(
            username=username,
            first_name=first_name,
            surname=surname,
            email=email,
            secondary_email=secondary_email,
            phone_number=phone_number,
            designation=designation
        )
        db.session.add(t)
        db.session.commit()
        return t

    def test_teacher(self):
        # Nice teacher who knows what should go where
        t_in = self.create_teacher()
        t = Teacher.query.get(1)
        self.assertEquals(t.first_name, t_in.first_name)
        self.assertEquals(t.surname, t_in.surname)
        #self.assertEquals(t.avatar,,)
        self.assertEquals(t.email, t_in.email)
        self.assertEquals(t.secondary_email, t_in.secondary_email)
        self.assertEquals(t.phone_number, t_in.phone_number)
        self.assertEquals(t.designation, t_in.designation)

        # Evil teachers who should be stopped
        self.assertRaises(IntegrityError, self.create_teacher, username=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_teacher, first_name=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_teacher, surname=None)
        db.session.rollback()
        self.assertRaises(ValueError, setattr, t, 'email', "Not an email address")
        self.assertRaises(ValueError, setattr, t, 'secondary_email', "Not an email address either")
        self.assertRaises(ValueError, setattr, t, 'phone_number', "Not a phone number")
        self.assertRaises(ValueError, setattr, t, 'designation', "Not a slug")

        # cleanup
        db.session.delete(t)
        db.session.commit()

    def test_login(self):
        ...

    def test_logout(self):
        ...

    def test_profile_page(self):
        ...

    def test_settings_page(self):
        ...

    def test_group(self):
        ...

    def test_group_page(self):
        ...

    def test_permission(self):
        ...

suite = unittest.makeSuite(UserTests)
