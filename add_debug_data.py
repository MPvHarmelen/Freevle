from datetime import date, timedelta

from freevle import db, app
# from freevle.blueprints.cms.tests import CMSTests
from freevle.blueprints.cms.models import Category, Subcategory, Page, TextSection, ImageSection, Event
from freevle.blueprints.news.models import NewsItem
# from freevle.blueprints.news.models import NewsItem, Event
# from freevle.blueprints.galleries.models import Album

NUMBER_OF_CATEGORIES = 7
NUMBER_OF_SUBCATEGORIES_PER_CATEGORIE = 3
NUMBER_OF_PAGES_PER_SUBCATEGORIE = 4
NUMBER_OF_UNPROTECTED_CATEGORIES = 1
NUMBER_OF_TEACHER_PROTECTED_CATEGORIES = 2
NUMBER_OF_EVENTS = 100
NUMBER_OF_NEWS_ITEMS = 100

image_urls = ['/static/img/sections/' + name for name in ['page.jpg', 'newsfront.png', 'page2.jpg']]
html_classes = ['school', 'education', 'activities', 'intern', 'more', 'promotion']

db.create_all()

page_content = "Aan het eind van elk {0} houden we enquêtes onder alle "\
"{0} en leerlingen. Door de jaren heen is het 'rapportcijfer' dat de ouders "\
"het Cygnus Gymnasium geven voor {0} en veiligheid heel goed - en daar zijn "\
"we trots op."

lorum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac viverra neque. Nulla quis erat tincidunt ipsum porttitor posuere fermentum a elit. Curabitur sit amet molestie dolor, a elementum lacus. Ut aliquam nec neque vel mollis. Integer at tortor imperdiet, dapibus eros ac, dictum orci. Integer sit amet orci ac tortor auctor vestibulum. Donec quis neque accumsan, scelerisque erat a, viverra lorem. Vivamus eleifend iaculis vehicula. Integer pellentesque tincidunt nulla vitae sollicitudin. Aliquam erat volutpat.

Vestibulum sodales molestie ligula a consectetur. Praesent eleifend, sem non auctor ultricies, massa sem dictum nibh, vitae tempor elit dui eu augue. Suspendisse imperdiet risus et libero molestie pellentesque. Aliquam gravida nibh nunc, at ultricies elit tincidunt at. Morbi non sem tempor, semper leo a, pulvinar lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan a sapien eget hendrerit. Duis urna erat, tincidunt at tincidunt in, faucibus et felis. In hac habitasse platea dictumst. Curabitur eleifend ante sit amet neque luctus, sit amet dictum nulla vestibulum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."""


# cms_tests = CMSTests()
def create_page_data(cat_amount, subcat_amount, page_amount):
    for cat_num in range(cat_amount):
        cat_name = 'test-{}'.format(cat_num)
        if cat_num < NUMBER_OF_UNPROTECTED_CATEGORIES:
            security_level = None
        elif cat_amount - cat_num <= NUMBER_OF_TEACHER_PROTECTED_CATEGORIES:
            security_level = 'teacher'
        else:
            security_level = 'student'
        cat = Category(
            title=cat_name,
            slug=cat_name,
            html_class=html_classes[cat_num % len(html_classes)],
            security_level=security_level
        )
        db.session.add(cat)
        print('Added category:\t', cat)
        for subcat_num in range(subcat_amount):
            subcat_name = 'test-{}'.format(subcat_num)
            subcat = Subcategory(
                title=subcat_name,
                slug=subcat_name,
                category=cat,
                html_class=html_classes[(cat_num + subcat_num) % len(html_classes)] if not security_level else None
            )
            db.session.add(subcat)
            print('Added subcategory:\t', subcat)
            for page_num in range(page_amount):
                p = Page(
                    subcategory=subcat,
                    title='TeSt{}'.format(page_num),
                    slug='test{}-{}'.format(subcat_num, page_num),
                    content=page_content.format(page_num),
                    cover_image_url=image_urls[(page_num + subcat_num + cat_num) % len(image_urls)],
                    is_published=True
                )
                db.session.add(p)
                print('Added page:\t', p)
                for y in range(2):
                    s = TextSection(
                        order=y,
                        title='section-{}'.format(y),
                        slug='section-{}'.format(y),
                        page=p,
                        content=lorum)
                    db.session.add(s)
                    print('Added section:\t', s)
                s = ImageSection(
                    order=2,
                    title='image1',
                    slug='image1',
                    page=p,
                    image_url=image_urls[1]
                )
                db.session.add(s)
                print('Added section:\t', s)
                s = TextSection(
                    order=3,
                    title='section-2',
                    slug='section-2',
                    page=p,
                    content=lorum
                )
                db.session.add(s)
                print('Added section:\t', s)
                s = ImageSection(
                    order=4,
                    title='image2',
                    slug='image2',
                    page=p,
                    image_url=image_urls[2]
                )
                db.session.add(s)
                print('Added section:\t', s)
                s = TextSection(
                    order=5,
                    title='section-3',
                    slug='section-3',
                    page=p,
                    content=lorum
                )
                db.session.add(s)
                print('Added section:\t', s)
    print('Commit!')
    db.session.commit()

def create_events(number):
    today = date.today()
    for num in range(number):
        event = Event(title='Nice event', date=today + timedelta(days=num))
        db.session.add(event)
        print('Added {} to session.'.format(event))
    print('Commit!')
    db.session.commit()

def create_news(amount):
    today = date.today()
    for num in range(amount):
        item = NewsItem(
            title='NewsItem {}'.format(num),
            slug='NewsItem-{}'.format(num),
            content=lorum,
            cover_image_url=(image_urls[num % len(image_urls)], None)[num % 2],
            date_published=today + timedelta(days=num)
        )
        db.session.add(item)
        print('Added {} to session.'.format(item))
    print('Commit!')
    db.session.commit()

if __name__ == '__main__':
    if input('Create page data? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        with app.app_context():
            create_page_data(NUMBER_OF_CATEGORIES,
                             NUMBER_OF_SUBCATEGORIES_PER_CATEGORIE,
                             NUMBER_OF_PAGES_PER_SUBCATEGORIE)
    if input('Create events? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        create_events(NUMBER_OF_EVENTS)
    if input('Create news? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        create_news(NUMBER_OF_NEWS_ITEMS)
    print('Done.')
