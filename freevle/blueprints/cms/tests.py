from time import sleep
import unittest
from datetime import datetime, timedelta
from freevle import db
from freevle.testing import TestBase
from freevle.utils.functions import headles_markdown
from sqlalchemy.exc import IntegrityError
from .models import Category, Subcategory, Page, TextSection, ImageSection, Link

ONUPDATE_DELTA = timedelta(microseconds=30000)
SLEEP_TIME = 1

class CMSTests(TestBase):
    def test_index(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status, '200 OK')

    @staticmethod
    def create_category(title, slug, html_class=''):
        cat = Category(title=title, slug=slug, html_class=html_class)
        db.session.add(cat)
        db.session.commit()
        return cat

    def test_category(self):
        # Create legal categories
        self.create_category('Te sT', 'test', 'classss')
        cat_got = Category.query.get(1)
        self.assertEqual(cat_got.title, 'Te sT')
        self.assertEqual(cat_got.slug, 'test')
        self.assertEqual(cat_got.html_class, 'classss')
        with self.app.app_context():
            self.assertEqual(cat_got.get_url(), 'http://' + self.app.config['SERVER_NAME'] + '/test/')
        self.assertEqual(self.client.get('/test/').status, '200 OK')
        # TODO: Test creating illegal categories

    @staticmethod
    def create_subcategory(title, slug, html_class='', user_type_view=None,
                           category=None, category_id=None):
        sub = Subcategory(
            title=title,
            slug=slug,
            html_class=html_class,
            user_type_view=user_type_view
        )

        if category is not None:
            sub.category = category
        elif category_id is not None:
            sub.category_id = subcategory_id
        else:
            raise TypeError("create_subcategory() missing one of either required "
                            "arguments: 'category', 'category_id'")
        db.session.add(sub)
        db.session.commit()
        return sub

    def test_subcategory(self):
        # Create legal subcategories
        cat = self.create_category('test', 'test')
        self.create_subcategory('Te sT', 'test', '#123456', 'parent', cat)
        subcat_got = Subcategory.query.get(1)
        self.assertEqual(subcat_got.title, 'Te sT')
        self.assertEqual(subcat_got.slug, 'test')
        self.assertEqual(subcat_got.html_class, '#123456')
        self.assertEqual(subcat_got.user_type_view, 'parent')
        self.assertEqual(subcat_got.category_id, cat.id)
        self.assertEqual(subcat_got.category, cat)

        # TODO: test creating illegal subcategories

    @staticmethod
    def create_page(title, slug, subcategory=None, subcategory_id=None,
                    content='Content.', is_published=True, cover_image_url=None):
        page = Page(
            title=title,
            slug=slug,
            content=content,
            is_published=is_published,
            cover_image_url=cover_image_url
        )
        if subcategory is not None:
            page.subcategory = subcategory
        elif subcategory_id is not None:
            page.subcategory_id = subcategory_id
        else:
            raise TypeError("create_page() missing one of either required "
                            "arguments: 'subcategory', 'subcategory_id'")
        db.session.add(page)
        db.session.commit()
        return page


    @staticmethod
    def create_text_section(title='TiTle', slug='title', order=0,
                            content='content.', page=None, page_id=None):
        ts = TextSection(
            title=title,
            slug=slug,
            order=order,
            content=content
        )
        if page is not None:
            ts.page = page
        elif page_id is not None:
            ts.page_id = page_id
        else:
            raise TypeError("create_text_section() missing one of either "
                            "required arguments: 'page', 'page_id'")
        db.session.add(ts)
        db.session.commit()
        return ts

    def test_text_section(self):
        # Create legal text sections
        cat = self.create_category('test', 'test')
        sub_cat = self.create_subcategory('test', 'test', '#123456', category=cat)
        page = self.create_page('TeSt', 'test', sub_cat)
        ts = self.create_text_section(page=page)
        ts_got = TextSection.query.get(1)
        self.assertEqual(ts_got.title, 'TiTle')
        self.assertEqual(ts_got.order, 0)
        self.assertEqual(ts_got.content, 'content.')
        self.assertEqual(ts_got.page, page)

        # TODO: create illegal text_sections

    @staticmethod
    def create_image_section(title='TiTle', slug='slug', order=0, image_url='path', page=None,
                             page_id=None):
        ims = ImageSection(
            title=title,
            slug=slug,
            image_url=image_url,
            order=order
        )

        if page is not None:
            ims.page = page
        elif page_id is not None:
            ims.page_id = page_id
        else:
            raise TypeError("create_image_section() missing one of either "
                            "required arguments: 'page', 'page_id'")
        db.session.add(ims)
        db.session.commit()
        return ims

    def test_image_section(self):
        ...

    def test_page(self):
        # Create legal pages
        cat = self.create_category('test', 'test')
        sub_cat = self.create_subcategory('test', 'test', '#123456', category=cat)
        sub_cat2 = self.create_subcategory('test', 'tesst', '#123456', category=cat)
        _ = self.create_page('TeSt', 'test', sub_cat2)
        p_in = self.create_page('TeSt', 'test', sub_cat, content='# Content.')
        now = datetime.now()
        text_section1 = self.create_text_section(page=p_in)
        image_section1 = self.create_image_section(order=1, slug='title1', page=p_in)
        text_section2 = self.create_text_section(order=2, slug='title2', page=p_in)
        image_section2 = self.create_image_section(order=3, slug='title3', page=p_in)
        all_sections = [text_section1, image_section1, text_section2, image_section2]
        p_got = Page.query.get(2)
        self.assertAlmostEqual(p_got.datetime_created, now, delta=ONUPDATE_DELTA)
        self.assertAlmostEqual(p_got.last_edited, now, delta=ONUPDATE_DELTA)
        self.assertEqual(p_got.title, 'TeSt')
        self.assertEqual(p_got.slug, 'test')
        self.assertEqual(p_got.content, '# Content.')
        self.assertEqual(headles_markdown(p_got.content), '<p>Content.</p>')
        self.assertEqual(p_got.subcategory_id, sub_cat.id)
        self.assertEqual(p_got.subcategory, sub_cat)
        self.assertEqual(p_got.is_published, True)
        self.assertEqual(p_got.sections.all(), all_sections)
        self.assertEqual(p_got.text_sections.all(), [text_section1, text_section2])
        self.assertEqual(p_got.image_sections.all(), [image_section1, image_section2])
        with self.app.app_context():
            self.assertEqual(
                p_got.get_url(),
                'http://' + self.app.config['SERVER_NAME'] + '/test/test/test'
            )
            self.assertEqual(
                p_got.get_edit_url(),
                'http://' + self.app.config['SERVER_NAME'] + '/admin/cms/page/test/test/test/edit'
            )
        self.assertEqual(self.client.get('/test/test/test').status, '200 OK')
        # Test if the 'last_edited' actually updates.
        last_edited = p_got.last_edited
        sleep(SLEEP_TIME)
        p_got.title = 'Something different.'
        db.session.add(p_got)
        db.session.commit()
        self.assertNotAlmostEqual(p_got.last_edited, last_edited, delta=timedelta(seconds=SLEEP_TIME))
        # Test if the datetime_created hasn't changed
        self.assertAlmostEqual(p_got.datetime_created, last_edited, delta=ONUPDATE_DELTA)
        # Test if the datetime_created isn't the same as last_edited
        self.assertNotAlmostEqual(p_got.datetime_created, p_got.last_edited, delta=ONUPDATE_DELTA)

        # Create illegal pages
        # Incorrect slug
        self.assertRaises(ValueError, self.create_page, 'title',
                          "This isn't a slug", sub_cat)

    @staticmethod
    def create_link(link=None, **kwargs):
        l = Link(link, **kwargs)
        db.session.add(l)
        db.session.commit()
        return l

    def test_link(self):
        cat = self.create_category('test', 'test', html_class='classss')
        assertRaisesTypeError = self.assertRaises(TypeError)
        with assertRaisesTypeError: Link()
        with assertRaisesTypeError: Link('category')
        with assertRaisesTypeError: Link(a=cat)
        with assertRaisesTypeError: Link(category=cat, category_id=cat.id)
        with assertRaisesTypeError: Link(id=1)
        with assertRaisesTypeError: Link('category', id=1)
        with assertRaisesTypeError: Link(a=cat, id=1)
        with assertRaisesTypeError: Link(category=cat, category_id=cat.id, id=1)

        with self.assertRaises(ValueError): Link(category=None)
        with self.assertRaises(ValueError): Link(id=1, category=None)

        with self.assertRaises(AttributeError): Link(category='aaaa')
        with self.assertRaises(AttributeError): Link(id=1, category='aaaa')

        get_db_link = lambda link: Link.query.get(link.id)
        def assertEqualCat(*args, **kwargs):
            return self.assertEqual(
                        get_db_link(
                            self.create_link(*args, **kwargs)
                        ).link,
                        cat
                   )

        assertEqualCat(cat, id=1)
        assertEqualCat(category=cat, id=2)
        assertEqualCat(category_id=cat.id, id=3)
        assertEqualCat(cat)
        assertEqualCat(category=cat)
        assertEqualCat(category_id=cat.id)

        sub = self.create_subcategory('title', 'slug', 'html_class', category=cat)
        link = self.create_link(sub)
        self.assertEquals(link.html_class, sub.html_class)
        with self.app.app_context():
            self.assertEqual(Link.query.get(1).get_url(), cat.get_url())
            self.assertEqual(link.get_url(), '')


suite = unittest.makeSuite(CMSTests)
