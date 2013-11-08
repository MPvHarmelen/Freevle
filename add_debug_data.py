from datetime import date, timedelta

from freevle import db, app
# from freevle.blueprints.cms.tests import CMSTests
from freevle.blueprints.cms.models import Category, Subcategory, Page, TextSection, ImageSection, Event
from freevle.blueprints.news.models import NewsItem
from freevle.blueprints.galleries.models import Album, Image

NUMBER_OF_CATEGORIES = 7
SUBCATEGORIES_PER_CATEGORIE = 3
PAGES_PER_SUBCATEGORIE = 4
NUMBER_OF_UNPROTECTED_CATEGORIES = 1
NUMBER_OF_TEACHER_PROTECTED_CATEGORIES = 2
NUMBER_OF_EVENTS = 100
NUMBER_OF_NEWS_ITEMS = 100
NUMBER_OF_ALBUMS = 100
IMAGES_PER_ALBUM = 100
TODAY = date.today()

def add(item):
    db.session.add(item)
    print('Added {} to session.'.format(item))

def commit():
    print('Commit!')
    db.session.commit()

image_urls = ['/static/img/' + name for name in ['page.jpg', 'newsfront.png', 'page2.jpg', 'paralax3.jpg', 'cover.png']]
html_classes = ['school', 'education', 'activities', 'intern', 'more', 'promotion']
authors = ['Floris Jansen', 'Pim ten Thije', 'Martin van Harmelen', 'Jan Modaal']

db.create_all()

page_content = "Aan het eind van elk {0} houden we enquêtes onder alle "\
"{0} en leerlingen. Door de jaren heen is het 'rapportcijfer' dat de ouders "\
"het Cygnus Gymnasium geven voor {0} en veiligheid heel goed - en daar zijn "\
"we trots op."

lorum = """Lorem _ipsum dolor_ sit amet, *consectetur* adipiscing elit. Donec ac __viverra__ neque. **Nulla quis** erat tincidunt ipsum porttitor posuere fermentum a elit. Curabitur sit amet molestie dolor, a elementum lacus. Ut aliquam nec neque vel mollis. Integer at tortor imperdiet, dapibus eros ac, dictum orci. Integer sit amet orci ac tortor auctor vestibulum. Donec quis neque accumsan, scelerisque erat a, viverra lorem. Vivamus eleifend iaculis vehicula. Integer pellentesque tincidunt nulla vitae sollicitudin. Aliquam erat volutpat.

# Vestibulum
sodales molestie ligula a consectetur. Praesent eleifend, sem non auctor ultricies, massa sem dictum nibh, vitae tempor elit dui eu augue. Suspendisse imperdiet risus et libero molestie pellentesque. Aliquam gravida nibh nunc, at ultricies elit tincidunt at. Morbi non sem tempor, semper leo a, pulvinar lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan a sapien eget hendrerit. Duis urna erat, tincidunt at tincidunt in, faucibus et felis. In hac habitasse platea dictumst. Curabitur eleifend ante sit amet neque luctus, sit amet dictum nulla vestibulum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."""

lorum_with_image = """Lorem _ipsum dolor_ sit amet, *consectetur* adipiscing elit. Donec ac __viverra__ neque. **Nulla quis** erat tincidunt ipsum porttitor posuere fermentum a elit. Curabitur sit amet molestie dolor, a elementum lacus. Ut aliquam nec neque vel mollis. Integer at tortor imperdiet, dapibus eros ac, dictum orci. Integer sit amet orci ac tortor auctor vestibulum. Donec quis neque accumsan, scelerisque erat a, viverra lorem. Vivamus eleifend iaculis vehicula. Integer pellentesque tincidunt nulla vitae sollicitudin. Aliquam erat volutpat.

![ImageIne]({} 'This is image')

# Vestibulum
sodales molestie ligula a consectetur. Praesent eleifend, sem non auctor ultricies, massa sem dictum nibh, vitae tempor elit dui eu augue. Suspendisse imperdiet risus et libero molestie pellentesque. Aliquam gravida nibh nunc, at ultricies elit tincidunt at. Morbi non sem tempor, semper leo a, pulvinar lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan a sapien eget hendrerit. Duis urna erat, tincidunt at tincidunt in, faucibus et felis. In hac habitasse platea dictumst. Curabitur eleifend ante sit amet neque luctus, sit amet dictum nulla vestibulum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."""

def create_page_data(cat_amount, subcat_amount, page_amount):
    for cat_num in range(cat_amount):
        cat_short_name = cat_name = 'cat-{}'.format(cat_num)
        if cat_num < NUMBER_OF_UNPROTECTED_CATEGORIES:
            security_level = None
            cat_name, cat_short_name = 'Category {}'.format(cat_num), cat_name
        elif cat_amount - cat_num <= NUMBER_OF_TEACHER_PROTECTED_CATEGORIES:
            security_level = 'teacher'
        else:
            security_level = 'student'
        cat = Category(
            title=cat_name,
            short_title=cat_short_name,
            slug=cat_short_name,
            html_class=html_classes[cat_num % len(html_classes)],
            security_level=security_level
        )
        add(cat)
        for subcat_num in range(subcat_amount):
            subcat_name = 'sub-{}'.format(subcat_num)
            subcat = Subcategory(
                title=subcat_name,
                slug=subcat_name,
                category=cat,
                html_class=html_classes[(cat_num + subcat_num) % len(html_classes)] if not security_level else None
            )
            add(subcat)
            for page_num in range(page_amount):
                p = Page(
                    subcategory=subcat,
                    title='Page{}'.format(page_num),
                    slug='page{}-{}'.format(subcat_num, page_num),
                    content=page_content.format(page_num),
                    cover_image_url=image_urls[(page_num + subcat_num + cat_num) % len(image_urls)],
                    is_published=True
                )
                add(p)
                for y in range(2):
                    add(TextSection(
                        order=y,
                        title='section-{}'.format(y),
                        slug='section-{}'.format(y),
                        page=p,
                        content=lorum))
                add(ImageSection(
                    order=2,
                    title='image1',
                    slug='image1',
                    page=p,
                    image_url=image_urls[1]
                ))
                add(TextSection(
                    order=3,
                    title='section-2',
                    slug='section-2',
                    page=p,
                    content=lorum_with_image.format(image_urls[
                        (page_num + subcat_num + cat_num) % len(image_urls)
                    ])
                ))
                add(ImageSection(
                    order=4,
                    title='image2',
                    slug='image2',
                    page=p,
                    image_url=image_urls[2]
                ))
                add(TextSection(
                    order=5,
                    title='section-3',
                    slug='section-3',
                    page=p,
                    content=lorum
                ))
    commit()

def create_events(number):
    for num in range(number):
        add(Event(title='Nice event', date=TODAY + timedelta(days=num)))
    commit()

def create_news(amount):
    for num in range(amount):
        add(NewsItem(
            title='NewsItem {}'.format(num),
            slug='NewsItem-{}'.format(num),
            author=authors[num % len(authors)],
            content=lorum_with_image.format(image_urls[(num + 1) % len(image_urls)]),
            cover_image_url=(image_urls[num % len(image_urls)], None)[num % 2],
            date_published=TODAY - timedelta(days=num)
        ))
    commit()

def create_albums(album_amount, image_amount):
    for album_num in range(album_amount):
        name = 'album-{}'.format(album_num)
        album = Album(
            title=name,
            slug=name,
            author=authors[album_num % len(authors)],
            description=lorum,
            date_published=TODAY - timedelta(days=100 * album_num)
        )
        add(album)
        for image_num in range(image_amount):
            name = 'image-{}'.format(image_num)
            add(Image(
                title=name,
                slug=name,
                album=album,
                order=image_num,
                image_url=image_urls[(image_num + album_num) % len(image_urls)]
            ))
    commit()

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('configuration', help='Relative path to configuration file', nargs='?')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose option.')
    parsed_args = parser.parse_args()

    print = print if parsed_args.verbose else lambda *args, **kwargs: None
    # def print(*args, **kwargs):
    #     if parsed_args.verbose: old_print(*args, **kwargs)

    if input('Create page data? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        with app.app_context():
            create_page_data(NUMBER_OF_CATEGORIES,
                             SUBCATEGORIES_PER_CATEGORIE,
                             PAGES_PER_SUBCATEGORIE)
    if input('Create events? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        create_events(NUMBER_OF_EVENTS)
    if input('Create news? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        create_news(NUMBER_OF_NEWS_ITEMS)
    if input('Create albums? (y/N) ').lower() in ['y', 'yes', 'yep', 'yeah']:
        create_albums(NUMBER_OF_ALBUMS, IMAGES_PER_ALBUM)
    print('Done.')
