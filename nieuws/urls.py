from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day, object_detail

from cygy.nieuws.models import NieuwsBericht

urlpatterns = patterns('',
    # Example:
    # (r'^cygy/', include('cygy.foo.urls')),
    (r'^$', archive_index,
        {'queryset': NieuwsBericht.objects.all(), 'date_field': 'publiceer', 'num_latest': 10}),

    (r'^(?P<year>\d{4})/', archive_year,
        {'queryset': NieuwsBericht.objects.all(), 'date_field': 'publiceer'}),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', archive_month,
        {'queryset': NieuwsBericht.objects.all(), 'date_field': 'publiceer'}),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', archive_day,
        {'queryset': NieuwsBericht.objects.all(), 'date_field': 'publiceer'}),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[-w]+)/$', object_detail,
        {'queryset': NieuwsBericht.objects.all(), 'date_field': 'publiceer'}, 'nieuwsbericht_detail'),
)
