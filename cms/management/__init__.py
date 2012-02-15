import random
from datetime import datetime

from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError

from cygy.cms import models
from cygy.settings import DEBUG
from cygy.custom.debug.markov import Markov

THIS_YEAR = datetime.today().year
NOW = datetime.now()

def debug_data(sender, **kwargs):
    verbosity = kwargs['verbosity']
    if verbosity > 1:
        print

    if not kwargs['interactive']:
        return
    else:
        cont = raw_input('Do you want to generate random pages (Y/n): ')
        if not cont.lower() in ('yes', 'y', '',):
            return

    # Create 500 news messages
    print ('Writing 3 insightful pages and subpages (this may take a while)'
            + (': ' if verbosity > 1 else '.'))

    if verbosity > 1:
        print ' Reading the complete works of William Shakespeare for inspiration.'
    file = open('custom/debug/shakespeare.txt')
    shakespeare = Markov(file)
    if verbosity > 1:
        print ' Writing pages'
    for i in xrange(3):
        title = shakespeare.generate_markov_text(1)
        slug = slugify(title)
        content = shakespeare.generate_markov_text(random.randint(400, 700))
        while True:
            p_year = random.randint(THIS_YEAR-10, THIS_YEAR)
            p_month = random.randint(1, 12)
            p_day = random.randint(1, 28)
            p_hour = random.randint(0, 23)
            p_minute = random.randint(0, 59)
            p_second = random.randint(0, 59)
            last_edit = datetime(p_year, p_month, p_day,
                    p_hour, p_minute, p_second)
            if last_edit < NOW:
                break
        parent = models.Page(title=title, last_edit=last_edit, slug=slug,
                content=content)
        parent.save()
        if verbosity > 1:
            print '- {}'.format(title)

        for i in xrange(random.randint(2, 5)):
            title = shakespeare.generate_markov_text(random.randint(1, 3))
            slug = slugify(title)
            content = shakespeare.generate_markov_text(random.randint(400, 700))
            while True:
                p_year = random.randint(THIS_YEAR-10, THIS_YEAR)
                p_month = random.randint(1, 12)
                p_day = random.randint(1, 28)
                p_hour = random.randint(0, 23)
                p_minute = random.randint(0, 59)
                p_second = random.randint(0, 59)
                last_edit = datetime(p_year, p_month, p_day,
                        p_hour, p_minute, p_second)
                if last_edit < NOW:
                    break
            sub = models.Page(parent=parent, title=title, slug=slug,
                    last_edit=last_edit, content=content)
            sub.save()
            if verbosity > 1:
                print '  - {} @ {}'.format(title, last_edit)

    file.close()
    if verbosity > 1:
        print

if DEBUG:
    post_syncdb.connect(debug_data, sender=models)

