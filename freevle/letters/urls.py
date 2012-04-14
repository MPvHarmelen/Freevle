from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index
from django.views.generic.simple import redirect_to

from freevle.letters.models import Letter

urlpatterns = patterns('',
    url(r'^$', archive_index,
        {'queryset': Letter.objects.all(), 'date_field': 'publish',
         'num_latest': 30}, name='letter-archive'),
)