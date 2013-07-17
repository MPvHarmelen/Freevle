import unittest
from freevle.testing import TestBase
from freevle import db

class CMSTests(TestBase):
    def test_index(self):
        rv = self.app.get('/')
        self.assertEquals(rv.status, 200)

    def create_page(self):
        ...

    def test_page(self):
        self.create_page()
        ...

suite = unittest.makeSuite(CMSTests)
