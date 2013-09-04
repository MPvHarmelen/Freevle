import unittest
from freevle.testing import TestBase
from freevle import db
from .models import Page
from datetime import datetime
class CMSTests(TestBase):
    def test_index(self):
        rv = self.app.get('/')
        self.assertEquals(rv.status, '200 OK')

    def create_page(self, title, slug, content, parent=None, parent_id=None):
        page = Page(
            title=title,
            slug=slug,
            parent=parent,
            parent_id=parent_id,
            content=content,
        )
        db.session.add(page)
        db.session.commit()
        return page

    def test_page(self):
        # Create legal pages
        self.create_page('TeSt', 'test', 'This is content.')
        p_got = Page.query.get(1)
        self.assertEquals(p_got.title, 'TeSt')
        self.assertEquals(p_got.slug, 'test')
        self.assertEquals(p_got.parent, None)
        self.assertEquals(p_got.content,'This is content.')

        self.create_page('TeSt2', 'test2', 'This is more content.', parent=p_got)
        child_got = Page.query.filter(Page.parent == p_got).first()
        self.assertEquals(child_got.title, 'TeSt2')
        self.assertEquals(child_got.slug, 'test2')
        self.assertEquals(child_got.content, 'This is more content.')
        self.assertEquals(child_got.parent_id, 1)
        self.assertEquals(child_got.parent, p_got)

        # Create illegal pages
        # Incorrect slug
        self.assertRaises(ValueError, self.create_page, 'title',
                          "This isn't a slug", 'Content.')
        # Child as parent
        self.assertRaises(ValueError, self.create_page, 'title',
                          'slug', 'Content.', child_got)

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
        self.assertEquals(from_db, original)


suite = unittest.makeSuite(CMSTests)
