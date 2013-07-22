import unittest
from freevle.testing import TestBase
from freevle import db
from .models import User, Group, Permission

from freevle.apps.cms.models import Page

class UserTests(TestBase):
    def add_and_commit(object):
        db.session.add(object)
        db.session.commit()

    def test_user(self):
        u_in = User(
            username='u',
            designation='u',
            first_name='u',
            surname='u',
            #avatar=,
            email='u@u.co'
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

        u_bad_email = u_bad_secondary_email = None
        u_bad_phone = u_bad_designation = None
        bad_li = [u_bad_email, u_bad_secondary_email, u_bad_phone,
                  u_bad_designation]

        for bad_u in bad_li:
            bad_u = User(
                username='u',
                designation='u',
                first_name='u',
                surname='u',
                #avatar=,
                email='u@u.co'
            )

        u_bad_email.email = "Not an email address"
        u_bad_secondary_email.secondary_email = "Not an email address either"
        u_bad_phone.phone_number = "Not a phone number"
        u_bad_designation.designation = "Not a slug"

        for bad_u in bad_li:
            assertRaises(ValueError, self.add_and_commit, bad_u)

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
