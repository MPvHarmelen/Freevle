from django.conf.urls.defaults import *
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView

from cygy.news.models import NewsMessage

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]*)/$',
        DateDetailView.as_view(
            queryset=NewsMessage.objects.all(), date_field='publish',
            month_format='%m'),
        name='newsmessage-detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(
            queryset=NewsMessage.objects.all(), date_field='publish',
            paginate_by=10, month_format='%m', allow_empty=True),
        name='newsmessage-day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            queryset=NewsMessage.objects.all(), date_field='publish',
            paginate_by=10, month_format='%m', allow_empty=True),
        name='newsmessage-month'),

    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset=NewsMessage.objects.all(), date_field='publish',
            paginate_by=10, allow_empty=True),
        name='newsmessage-year'),

    url(r'^$',
        ArchiveIndexView.as_view(
            queryset=NewsMessage.objects.all(), date_field='publish',
            paginate_by=10),
        name='newsmessage-archive'),
)

