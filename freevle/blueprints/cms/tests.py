from time import sleep
import unittest
from datetime import datetime, timedelta
from freevle import db
from freevle.testing import TestBase
from sqlalchemy.exc import IntegrityError
from .models import Category, Subcategory, Page, TextSection, ImageSection

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
    def create_page(title, slug, subcategory=None, subcategory_id=None, content='Content.', is_published=True):
        page = Page(
            title=title,
            slug=slug,
            content=content,
            is_published=is_published
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
    def create_text_section(title='TiTle', order=0, content='content.',
                            page=None, page_id=None):
        ts = TextSection(
            title=title,
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
    def create_image_section(title='TiTle', order=0, image_path='path', page=None,
                             page_id=None):
        ims = ImageSection(
            title=title,
            image_path=image_path,
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
        p_in = self.create_page('TeSt', 'test', sub_cat)
        now = datetime.now()
        text_section1 = self.create_text_section(page=p_in)
        image_section1 = self.create_image_section(order=1, page=p_in)
        text_section2 = self.create_text_section(order=2, page=p_in)
        image_section2 = self.create_image_section(order=3, page=p_in)
        all_sections = [text_section1, image_section1, text_section2, image_section2]
        p_got = Page.query.get(2)
        self.assertAlmostEqual(p_got.datetime_created, now, delta=ONUPDATE_DELTA)
        self.assertAlmostEqual(p_got.last_edited, now, delta=ONUPDATE_DELTA)
        self.assertEqual(p_got.title, 'TeSt')
        self.assertEqual(p_got.slug, 'test')
        self.assertEqual(p_got.content, 'Content.')
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

        # self.create_page('TeSt2', 'test2', 'This is more content.', parent=p_got)
        # now = datetime.now()
        # child_got = Page.query.filter(Page.parent == p_got).first()
        # self.assertAlmostEqual(child_got.datetime_created, now, delta=ONUPDATE_DELTA)
        # self.assertAlmostEqual(child_got.last_edited, now, delta=ONUPDATE_DELTA)
        # self.assertEqual(child_got.title, 'TeSt2')
        # self.assertEqual(child_got.slug, 'test2')
        # self.assertEqual(child_got.content, 'This is more content.')
        # self.assertEqual(child_got.parent_id, 1)
        # self.assertEqual(child_got.parent, p_got)
        # with self.app.app_context():
        #     self.assertEqual(child_got.get_url(), 'http://' + self.app.config['SERVER_NAME'] + '/test/test2/')
        # self.assertEqual(self.client.get('/test/test2/').status, '200 OK')

        # Create illegal pages
        # Incorrect slug
        self.assertRaises(ValueError, self.create_page, 'title',
                          "This isn't a slug", sub_cat)

    # def test_order(self):
    #     parent = self.create_page('parent', 'parent', 'Content.')
    #     pages = ['t' + str(i) for i in range(10)]
    #     for i, page in enumerate(pages):
    #         pages[i] = self.create_page(page, page, 'Content.', parent)

    #     db.session.delete(Page.query.get(4))
    #     db.session.commit()
    #     # id=4 because parent has id 1 and python is zero based whereas
    #     # SQLAlchemy is not
    #     db.session.add(Page(
    #         id=4,
    #         title='t2',
    #         slug='t2',
    #         content='Content.',
    #         parent=parent
    #     ))
    #     db.session.commit()
    #     from_db = [page.id for page in parent.children.all()]
    #     original = [page.id for page in pages]
    #     self.assertEqual(from_db, original)


suite = unittest.makeSuite(CMSTests)
