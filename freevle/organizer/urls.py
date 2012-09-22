from django.conf.urls.defaults import *
from freevle.organizer.views import organizer_view

urlpatterns = patterns('',
    url(r'^(?P<slug>[\d\w-]+)/$', organizer_view, {},
        name='organizer'),
    url(r'^(?P<slug>[\d\w-]+)/(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$', organizer_view, {},
        name='organizer-date'),
)
