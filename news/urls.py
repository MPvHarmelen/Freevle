from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day, object_detail

from cygy.nieuws.models import NewsMessage

urlpatterns = patterns('',
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]*)/$', object_detail,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publiceer', 'month_format': '%m'}, 'nieuwsbericht-detail'),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', archive_day,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publiceer', 'month_format': '%m'}),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', archive_month,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publiceer', 'month_format': '%m'}),

    (r'^(?P<year>\d{4})/$', archive_year,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publiceer'}),

    (r'^$', archive_index,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publiceer', 'num_latest': 10}),
)
