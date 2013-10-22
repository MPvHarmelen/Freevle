from freevle import db
from freevle.blueprints.cms.models import Page
from freevle.blueprints.cms.tests import CMSTests
from freevle.blueprints.news.models import NewsItem, Event
from freevle.blueprints.galleries.models import Album

db.create_all()

page_content = "Aan het eind van elk {0} houden we enquêtes onder alle "\
"{0} en leerlingen. Door de jaren heen is het 'rapportcijfer' dat de ouders "\
"het Cygnus Gymnasium geven voor {0} en veiligheid heel goed - en daar zijn "\
"we trots op."

lorum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac viverra neque. Nulla quis erat tincidunt ipsum porttitor posuere fermentum a elit. Curabitur sit amet molestie dolor, a elementum lacus. Ut aliquam nec neque vel mollis. Integer at tortor imperdiet, dapibus eros ac, dictum orci. Integer sit amet orci ac tortor auctor vestibulum. Donec quis neque accumsan, scelerisque erat a, viverra lorem. Vivamus eleifend iaculis vehicula. Integer pellentesque tincidunt nulla vitae sollicitudin. Aliquam erat volutpat.

Vestibulum sodales molestie ligula a consectetur. Praesent eleifend, sem non auctor ultricies, massa sem dictum nibh, vitae tempor elit dui eu augue. Suspendisse imperdiet risus et libero molestie pellentesque. Aliquam gravida nibh nunc, at ultricies elit tincidunt at. Morbi non sem tempor, semper leo a, pulvinar lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan a sapien eget hendrerit. Duis urna erat, tincidunt at tincidunt in, faucibus et felis. In hac habitasse platea dictumst. Curabitur eleifend ante sit amet neque luctus, sit amet dictum nulla vestibulum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."""


image_urls = ['/static/img/sections/' + name for name in ['page.jpg', 'newsfront.png', 'page2.jpg']]

cms_tests = CMSTests()
cat = cms_tests.create_category('test', 'test')
sub_cat = cms_tests.create_subcategory('test', 'test', '#123456', category=cat)
for x in range(10):
    p = cms_tests.create_page('TeSt{}'.format(x), 'test{}'.format(x), sub_cat,
                              content=page_content.format(x),
                              cover_image_url=image_urls[x % 3])
    print('Made page: ', p)
    for y in range(2):
        s = cms_tests.create_text_section(order=y, slug='section-{}'.format(y),
                                      page=p, content=lorum)
        print('Made section:\t', s)
    s = cms_tests.create_image_section(order=2, slug='image1', page=p,
                                   image_url=image_urls[1])
    print('Made section:\t', s)
    s = cms_tests.create_text_section(order=3, slug='section-2'.format(y),
                                      page=p, content=lorum)
    print('Made section:\t', s)
    s = cms_tests.create_image_section(order=4, slug='image2', page=p,
                                   image_url=image_urls[2])
    print('Made section:\t', s)
    s = cms_tests.create_text_section(order=5, slug='section-3'.format(y),
                                      page=p, content=lorum)
    print('Made section:\t', s)
