from time import sleep
import unittest
from datetime import datetime, timedelta
from freevle import db
from freevle.testing import TestBase
from sqlalchemy.exc import IntegrityError
from .models import Page

ONUPDATE_DETLA = timedelta(microseconds=30000)
SLEEP_TIME = 1

class CMSTests(TestBase):
    def test_index(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status, '200 OK')

    def create_page(self, title, slug, content, parent=None, parent_id=None):
        page = Page(
            title=title,
            slug=slug,
            content=content,
        )
        if parent is not None:
            page.parent = parent
        elif parent_id is not None:
            page.parent_id = parent_id
        db.session.add(page)
        db.session.commit()
        return page

    def test_page(self):
        # Create legal pages
        self.create_page('TeSt', 'test', 'This is content.')
        p_got = Page.query.get(1)
        now = datetime.now()
        self.assertAlmostEqual(p_got.created, now, delta=ONUPDATE_DETLA)
        self.assertAlmostEqual(p_got.last_edited, now, delta=ONUPDATE_DETLA)
        self.assertEqual(p_got.title, 'TeSt')
        self.assertEqual(p_got.slug, 'test')
        self.assertEqual(p_got.parent, None)
        self.assertEqual(p_got.content,'This is content.')
        with self.app.app_context():
            self.assertEqual(p_got.get_url(), 'http://' + self.app.config['SERVER_NAME'] + '/test/')
        self.assertEqual(self.client.get('/test/').status, '200 OK')

        # Test if the 'last_edited' actually updates.
        last_edited = p_got.last_edited
        sleep(SLEEP_TIME)
        p_got.title = 'Something different.'
        db.session.add(p_got)
        db.session.commit()
        self.assertNotAlmostEqual(p_got.last_edited, last_edited, delta=timedelta(seconds=SLEEP_TIME))
        # Test if the created hasn't changed
        self.assertAlmostEqual(p_got.created, last_edited, delta=ONUPDATE_DETLA)

        self.create_page('TeSt2', 'test2', 'This is more content.', parent=p_got)
        child_got = Page.query.filter(Page.parent == p_got).first()
        now = datetime.now()
        self.assertAlmostEqual(child_got.created, now, delta=ONUPDATE_DETLA)
        self.assertAlmostEqual(child_got.last_edited, now, delta=ONUPDATE_DETLA)
        self.assertEqual(child_got.title, 'TeSt2')
        self.assertEqual(child_got.slug, 'test2')
        self.assertEqual(child_got.content, 'This is more content.')
        self.assertEqual(child_got.parent_id, 1)
        self.assertEqual(child_got.parent, p_got)
        with self.app.app_context():
            self.assertEqual(child_got.get_url(), 'http://' + self.app.config['SERVER_NAME'] + '/test/test2/')
        self.assertEqual(self.client.get('/test/test2/').status, '200 OK')

        # Create illegal pages
        # Incorrect slug
        self.assertRaises(ValueError, self.create_page, 'title',
                          "This isn't a slug", 'Content.')

        # Child as parent
        self.assertRaises(ValueError, self.create_page, 'title',
                          'slug', 'Content.', child_got)
        db.session.rollback()

        # Duplicate (parent, slug) combination
        self.assertRaises(IntegrityError, self.create_page, p_got.title,
                          p_got.slug, p_got.content)
        db.session.rollback()


    def test_order(self):
        parent = self.create_page('parent', 'parent', 'Content.')
        pages = ['t' + str(i) for i in range(10)]
        for i, page in enumerate(pages):
            pages[i] = self.create_page(page, page, 'Content.', parent)

        db.session.delete(Page.query.get(4))
        db.session.commit()
        # id=4 because parent has id 1 and python is zero based whereas
        # SQLAlchemy is not
        db.session.add(Page(
            id=4,
            title='t2',
            slug='t2',
            content='Content.',
            parent=parent
        ))
        db.session.commit()
        from_db = [page.id for page in parent.children.all()]
        original = [page.id for page in pages]
        self.assertEqual(from_db, original)


suite = unittest.makeSuite(CMSTests)
