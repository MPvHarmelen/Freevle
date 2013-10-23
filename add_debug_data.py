from freevle import db
from freevle.blueprints.cms.tests import CMSTests
# from freevle.blueprints.news.models import NewsItem, Event
# from freevle.blueprints.galleries.models import Album

NUMBER_OF_CATEGORIES = 7
NUMBER_OF_SUBCATEGORIES_PER_CATEGORIE = 3
NUMBER_OF_PAGES_PER_SUBCATEGORIE = 4
NUMBER_OF_UNPROTECTED_CATEGORIES = 1
NUMBER_OF_TEACHER_PROTECTED_CATEGORIES = 2

db.create_all()

page_content = "Aan het eind van elk {0} houden we enquêtes onder alle "\
"{0} en leerlingen. Door de jaren heen is het 'rapportcijfer' dat de ouders "\
"het Cygnus Gymnasium geven voor {0} en veiligheid heel goed - en daar zijn "\
"we trots op."

lorum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac viverra neque. Nulla quis erat tincidunt ipsum porttitor posuere fermentum a elit. Curabitur sit amet molestie dolor, a elementum lacus. Ut aliquam nec neque vel mollis. Integer at tortor imperdiet, dapibus eros ac, dictum orci. Integer sit amet orci ac tortor auctor vestibulum. Donec quis neque accumsan, scelerisque erat a, viverra lorem. Vivamus eleifend iaculis vehicula. Integer pellentesque tincidunt nulla vitae sollicitudin. Aliquam erat volutpat.

Vestibulum sodales molestie ligula a consectetur. Praesent eleifend, sem non auctor ultricies, massa sem dictum nibh, vitae tempor elit dui eu augue. Suspendisse imperdiet risus et libero molestie pellentesque. Aliquam gravida nibh nunc, at ultricies elit tincidunt at. Morbi non sem tempor, semper leo a, pulvinar lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan a sapien eget hendrerit. Duis urna erat, tincidunt at tincidunt in, faucibus et felis. In hac habitasse platea dictumst. Curabitur eleifend ante sit amet neque luctus, sit amet dictum nulla vestibulum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."""


image_urls = ['/static/img/sections/' + name for name in ['page.jpg', 'newsfront.png', 'page2.jpg']]
html_classes = ['school', 'education', 'activities', 'intern', 'more', 'promotion']

cms_tests = CMSTests()
for cat_num in range(NUMBER_OF_CATEGORIES):
    cat_name = 'test-{}'.format(cat_num)
    if cat_num < NUMBER_OF_UNPROTECTED_CATEGORIES:
        security_level = None
    elif NUMBER_OF_CATEGORIES - cat_num <= NUMBER_OF_TEACHER_PROTECTED_CATEGORIES:
        security_level = 'teacher'
    else:
        security_level = 'student'
    cat = cms_tests.create_category(
        cat_name,
        cat_name,
        html_classes[cat_num % len(html_classes)],
        security_level
    )
    print('Made category:\t', cat)
    for subcat_num in range(NUMBER_OF_SUBCATEGORIES_PER_CATEGORIE):
        subcat_name = 'test-{}'.format(subcat_num)
        subcat = cms_tests.create_subcategory(
            subcat_name,
            subcat_name,
            category=cat,
            html_class=html_classes[(cat_num + subcat_num) % len(html_classes)] if not security_level else None
        )
        print('Made subcategory:\t', subcat)
        for page_num in range(NUMBER_OF_PAGES_PER_SUBCATEGORIE):
            p = cms_tests.create_page(
                'TeSt{}'.format(page_num),
                'test{}'.format(page_num),
                subcat,
                content=page_content.format(page_num),
                cover_image_url=image_urls[(page_num + subcat_num + cat_num) % len(image_urls)]
            )
            print('Made page:\t', p)
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

print('Done.')
