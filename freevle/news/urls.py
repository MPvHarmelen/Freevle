from django.conf.urls.defaults import *
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import MonthArchiveView, DayArchiveView
from django.views.generic.dates import DateDetailView

from schoolr.news.models import NewsMessage

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]*)/$',
        DateDetailView.as_view(
            model=NewsMessage, date_field='publish', month_format='%m',
            context_object_name='message'),
        name='newsmessage-detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(
            model=NewsMessage, date_field='publish', paginate_by=10,
            month_format='%m', allow_empty=True,
            context_object_name='message_list'
            ),
        name='newsmessage-day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            model=NewsMessage, date_field='publish', paginate_by=10,
            month_format='%m', allow_empty=True,
            context_object_name='message_list'
            ),
        name='newsmessage-month'),

    url(r'^$',
        ArchiveIndexView.as_view(
            queryset=NewsMessage.objects.all(), date_field='publish',
            paginate_by=10, allow_empty=True),
        name='newsmessage-archive'),
)

