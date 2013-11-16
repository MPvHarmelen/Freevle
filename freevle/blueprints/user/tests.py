import unittest
from freevle.testing import TestBase
from freevle import db
from sqlalchemy.exc import IntegrityError
from .models import Permission, Group, User, Admin, Teacher, Parent, Student

class UserTests(TestBase):
    """Tests for User blueprint."""

    def create_user(self, username='u', first_name='u', surname='u',
                    email='u@u.co', secondary_email='u@u.co',
                    phone_number='+0123456789'):
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

    def create_admin(self, username='a', first_name='a', surname='a',
                     email='a@a.co', secondary_email='a@a.co',
                     phone_number='+0123456789'):
        a = Admin(
            username=username,
            first_name=first_name,
            surname=surname,
            email=email,
            secondary_email=secondary_email,
            phone_number=phone_number
        )
        db.session.add(a)
        db.session.commit()
        return a

    def test_admin(self):
        # Nice admin who knows what should go where
        a_in = self.create_admin()
        a = Admin.query.get(1)
        self.assertEquals(a.username, a_in.username)
        self.assertEquals(a.first_name, a_in.first_name)
        self.assertEquals(a.surname, a_in.surname)
        #self.assertEquals(a.avatar,,)
        self.assertEquals(a.email, a_in.email)
        self.assertEquals(a.secondary_email, a_in.secondary_email)
        self.assertEquals(a.phone_number, a_in.phone_number)

        # Evil admins who should be stopped
        self.assertRaises(IntegrityError, self.create_admin, username=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_admin, first_name=None)
        db.session.rollback()
        self.assertRaises(IntegrityError, self.create_admin, surname=None)
        db.session.rollback()
        self.assertRaises(ValueError, setattr, a, 'email', "Not an email address")
        self.assertRaises(ValueError, setattr, a, 'secondary_email', "Not an email address either")
        self.assertRaises(ValueError, setattr, a, 'phone_number', "Not a phone number")

        # cleanup
        db.session.delete(a)
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
        self.assertEquals(t.username, t_in.username)
        self.assertEquals(t.first_name, t_in.first_name)
        self.assertEquals(t.surname, t_in.surname)
        #self.assertEquals(t.avatar,,)
        self.assertEquals(t.email, t_in.email)
        self.assertEquals(t.secondary_email, t_in.secondary_email)
        self.assertEquals(t.phone_number, t_in.phone_number)
        self.assertEquals(t.designation, t_in.designation)
        self.assertIsInstance(t, Parent)
        self.assertIsInstance(t, User)
        self.assertEquals(t.is_polymorphic_of('Teacher'), True)
        self.assertEquals(t.is_polymorphic_of('Parent'), True)
        self.assertEquals(t.is_polymorphic_of('User'), True)
        self.assertEquals(t.is_polymorphic_of('Student'), False)
        self.assertEquals(t.is_polymorphic_of('Admin'), False)
        self.assertRaises(ValueError, t.is_polymorphic_of, 'admin')
        self.assertRaises(ValueError, t.is_polymorphic_of, 'not an identity')

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

    # def create_parent_teacher(self, username='pt', first_name='pt', surname='pt',
    #                    email='pt@pt.co', secondary_email='pt@pt.co',
    #                    phone_number='+0123456789', designation='pt'):
    #     pt = ParentTeacher(
    #         username=username,
    #         first_name=first_name,
    #         surname=surname,
    #         email=email,
    #         secondary_email=secondary_email,
    #         phone_number=phone_number,
    #         designation=designation
    #     )
    #     db.session.add(pt)
    #     db.session.commit()
    #     return pt

    # def test_parent_teacher(self):
    #     # Nice parent_teacher who knows what should go where
    #     pt_in = self.create_parent_teacher()
    #     pt = ParentTeacher.query.get(1)
    #     self.assertEquals(pt.username, 'pt')
    #     self.assertEquals(pt.first_name, 'pt')
    #     self.assertEquals(pt.surname, 'pt')
    #     #self.assertEquals(pt.avatar,,)
    #     self.assertEquals(pt.email, 'pt@pt.co')
    #     self.assertEquals(pt.secondary_email, 'pt@pt.co')
    #     self.assertEquals(pt.phone_number, '+0123456789')
    #     self.assertEquals(pt.designation, 'pt')
    #     self.assertIsInstance(pt, Parent)
    #     self.assertIsInstance(pt, Teacher)
    #     self.assertNotIsInstance(pt, Admin)

    #     # Evil parent_teachers who should be stopped
    #     self.assertRaises(IntegrityError, self.create_parent_teacher, username=None)
    #     db.session.rollback()
    #     self.assertRaises(IntegrityError, self.create_parent_teacher, first_name=None)
    #     db.session.rollback()
    #     self.assertRaises(IntegrityError, self.create_parent_teacher, surname=None)
    #     db.session.rollback()
    #     self.assertRaises(ValueError, setattr, pt, 'email', "Not an email address")
    #     self.assertRaises(ValueError, setattr, pt, 'secondary_email', "Not an email address either")
    #     self.assertRaises(ValueError, setattr, pt, 'phone_number', "Not a phone number")
    #     self.assertRaises(ValueError, setattr, pt, 'designation', "Not a slug")

    #     # cleanup
    #     db.session.delete(pt)
    #     db.session.commit()

    def create_student(self, username='u', first_name='u', surname='u',
                       email='u@u.co', secondary_email='u@u.co',
                       phone_number='+0123456789', designation='u', year=1,
                       parents=[]):
        s = Student(
            username=username,
            first_name=first_name,
            surname=surname,
            email=email,
            secondary_email=secondary_email,
            phone_number=phone_number,
            designation=designation,
            year=year,
            parents=parents
        )
        db.session.add(s)
        db.session.commit()
        return s

    def test_student(self):
        # Nice student who knows what should go where
        parent = self.create_parent(username='parent')
        s_in = self.create_student(parents=[parent])
        s2 = self.create_student(parents=[parent], username='s2', designation='s2')
        s = Student.query.get(2)
        self.assertEquals(s.username, s_in.username)
        self.assertEquals(s.first_name, s_in.first_name)
        self.assertEquals(s.surname, s_in.surname)
        #self.assertEquals(s.avatar,,)
        self.assertEquals(s.email, s_in.email)
        self.assertEquals(s.secondary_email, s_in.secondary_email)
        self.assertEquals(s.phone_number, s_in.phone_number)
        self.assertEquals(s.designation, s_in.designation)
        self.assertEquals(s.year, s_in.year)
        self.assertEquals(s.parents.all(), [parent])
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

    # def test_login(self):
    #     ...

    # def test_logout(self):
    #     ...

    # def test_profile_page(self):
    #     ...

    # def test_settings_page(self):
    #     ...

    # def test_group(self):
    #     ...

    # def test_group_page(self):
    #     ...

    # def test_permission(self):
    #     ...

suite = unittest.makeSuite(UserTests)
