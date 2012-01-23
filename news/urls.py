from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day, object_detail

from cygy.news.models import NewsMessage

urlpatterns = patterns('',
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]*)/$',
        object_detail,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publish',
         'month_format': '%m', 'template_object_name': 'message'},
         'newsmessage-detail'),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', archive_day,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publish',
         'month_format': '%m', 'template_object_name': 'message'}),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', archive_month,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publish',
         'month_format': '%m', 'template_object_name': 'message'}),

    (r'^(?P<year>\d{4})/$', archive_year,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publish',
         'make_object_list':True, 'template_object_name': 'message'}),

    (r'^$', archive_index,
        {'queryset': NewsMessage.objects.all(), 'date_field': 'publish',
         'num_latest': 10}),
)
