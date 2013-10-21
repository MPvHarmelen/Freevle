from freevle import db
from freevle.blueprints.cms.models import Page
from freevle.blueprints.cms.tests import CMSTests
from freevle.blueprints.news.models import NewsItem, Event
from freevle.blueprints.galleries.models import Album

db.create_all()

cms_tests = CMSTests()
cat = cms_tests.create_category('test', 'test')
sub_cat = cms_tests.create_subcategory('test', 'test', '#123456', category=cat)
for x in range(10):
    p = cms_tests.create_page('TeSt{}'.format(x), 'test{}'.format(x), sub_cat)
    for y in range(3):
        cms_tests.create_text_section(order=y, page=p)
