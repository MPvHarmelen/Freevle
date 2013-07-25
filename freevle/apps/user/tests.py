import unittest
from freevle.testing import TestBase
from freevle import db
from .models import User, Group, Permission

class UserTests(TestBase):
    def test_user(self):
        # Nice user who knows what should go where
        u_in = User(
            username='u',
            designation='u',
            first_name='u',
            surname='u',
            #avatar=,
            email='u@u.co',
            secondary_email='u@u.co',
            phone_number='+0123456789'
        )
        db.session.add(u_in)
        db.session.commit()
        u = User.query.get(1)
        self.assertEquals(u.username,'u')
        self.assertEquals(u.designation,'u')
        self.assertEquals(u.first_name,'u')
        self.assertEquals(u.surname,'u')
        #self.assertEquals(u.avatar,,)
        self.assertEquals(u.email,'u@u.co')
        self.assertEquals(u.secondary_email,'u@u.co')
        self.assertEquals(u.phone_number,'+0123456789')

        # Evil users who should be stopped
        self.assertRaises(ValueError, setattr, u, 'email', "Not an email address")
        self.assertRaises(ValueError, setattr, u, 'secondary_email', "Not an email address either")
        self.assertRaises(ValueError, setattr, u, 'phone_number', "Not a phone number")
        self.assertRaises(ValueError, setattr, u, 'designation', "Not a slug")

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
