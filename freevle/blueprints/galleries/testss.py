import unittest
from freevle.testing import TestBase
from datetime import date, timedelta

from sqlalchemy.exc import IntegrityError

from freevle import db
from .models import Album, Image

TOWEL_DAY = date(2001, 5, 25)
class GalleriesTest(TestBase):

    @staticmethod
    def create_album(title='TeSt', slug='test', description='Description.',
                     date_published=TOWEL_DAY):
        a = Album(
            title=title,
            slug=slug,
            description=description,
            date_published=date_published
        )
        db.session.add(a)
        db.session.commit()
        return a

    def test_album(self):
        a = self.create_album()
        a_got = Album.query.get(1)

        # Test unique slug and year thing
        a_2 = self.create_album(date_published=TOWEL_DAY + timedelta(days=365))
        self.assertRaises(IntegrityError, self.create_album)

    @staticmethod
    def create_image(title='TeSt', slug='test', order=0, image_url='/bla/',
                     album_id=1):
        i = Image(
            title=title,
            slug=slug,
            album_id=album_id,
            order=order,
            image_url=image_url
        )
        db.session.add(i)
        db.session.commit()
        return i

    def test_cover_image(self):
        a = self.create_album()
        i = self.create_image()
        a.cover_image = i
        self.assertEquals(a.cover_image, i)

suite = unittest.makeSuite(GalleriesTest)
