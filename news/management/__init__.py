import random
import sys
from datetime import datetime

from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError

from cygy.news import models
from cygy.settings import DEBUG
from cygy.custom.debug.markov import Markov
from cygy.custom.progressbar import ProgressBar

THIS_YEAR = datetime.today().year
NOW = datetime.now()

def debug_data(sender, **kwargs):
    verbosity = kwargs['verbosity']
    if verbosity > 1:
        print

    if not kwargs['interactive']:
        return
    else:
        cont = raw_input('Do you want to generate 150 random news messages (Y/n): ')
        if not cont.lower() in ('yes', 'y', '',):
            return

    # Create 150 news messages
    print ('Writing 150 brilliant news messages (this may take a while)'
            + (': ' if verbosity > 1 else '.'))

    if verbosity > 1:
        print ' Reading the complete works of William Shakespeare for inspiration.'
    file = open('custom/debug/shakespeare.txt')
    shakespeare = Markov(file)
    if verbosity > 1:
        print ' Writing news messages'
    elif verbosity == 1:
        prog = ProgressBar(0, 150, 77, mode='fixed')
        print prog, '\r',

    for i in xrange(150):
        writer = User.objects.filter(groups__name='teachers').order_by('?')[0]
        title = shakespeare.generate_markov_text(random.randint(5, 10))
        content = shakespeare.generate_markov_text(random.randint(150, 400))
        while True:
            p_year = random.randint(THIS_YEAR-10, THIS_YEAR)
            p_month = random.randint(1, 12)
            p_day = random.randint(1, 28)
            p_hour = random.randint(0, 23)
            p_minute = random.randint(0, 59)
            p_second = random.randint(0, 59)
            publish = datetime(p_year, p_month, p_day,
                    p_hour, p_minute, p_second)
            if publish < NOW:
                break
        me = models.NewsMessage(writer=writer, title=title, slug=slugify(title),
                publish=publish, content=content)
        me.save()
        if verbosity > 1:
            print '- {} <{} @ {}>'.format(title, writer.get_full_name(),
                    publish)
        elif verbosity == 1:
            prog.increment_amount()
            print prog, '\r',
            sys.stdout.flush()
    file.close()
    print
    print

if DEBUG:
    post_syncdb.connect(debug_data, sender=models)

