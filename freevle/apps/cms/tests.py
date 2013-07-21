import unittest
from freevle.testing import TestBase
from freevle import db
from .models import Page
from datetime import datetime
class CMSTests(TestBase):
    def test_index(self):
        rv = self.app.get('/')
        self.assertEquals(rv.status, 200)

    def create_page(self, title, slug, content, last_edited, parent=None,
                    parent_id=None):
        db.session.add(Page(
            title=title,
            slug=slug,
            parent=parent,
            parent_id=parent_id,
            content=content,
            last_edited=last_edited
        ))
        db.session.commit()

    def test_page(self):
        # Create legal pages
        self.create_page('TeSt', 'test', 'This is content.',
                         datetime(2012, 12, 12))
        p_got = Page.query.get(1)
        self.assertEquals(p_got.title, 'TeSt')
        self.assertEquals(p_got.slug, 'test')
        self.assertEquals(p_got.parent, None)
        self.assertEquals(p_got.content,'This is content.')
        self.assertEquals(p_got.last_edited, datetime(2012, 12, 12))

        self.create_page('TeSt2', 'test2', 'This is more content.',
                         datetime(2011, 11, 11), parent=p_got)
        child_got = Page.query.filter(Page.parent == p_got).first()
        self.assertEquals(child_got.title, 'TeSt2')
        self.assertEquals(child_got.slug, 'test2')
        self.assertEquals(child_got.content, 'This is more content.')
        self.assertEquals(child_got.last_edited, datetime(2011, 11, 11))
        self.assertEquals(child_got.parent_id, 1)
        self.assertEquals(child_got.parent, p_got)

        # Create illegal pages
        self.assertRaises(ValueError, self.create_page, 'title',
                          "This isn't a slug", 'Content.', datetime.now())
        self.assertRaises(ValueError, self.create_page, 'title',
                          'slug', 'Content.', datetime.now(),
                          parent=child_got)
        db.session.close()

suite = unittest.makeSuite(CMSTests)
