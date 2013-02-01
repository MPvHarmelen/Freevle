from django.conf.urls.defaults import *
from freevle.organizer.views import organizer_view
from freevle.organizer.homework_views import GetCourseView, UpdateHomeworkView

urlpatterns = patterns('',
#    url(r'^homework-create/$', HomeworkCreate.as_view(), {},
#        name='homework-create'),
    url(r'^update-homework/$', GetCourseView.as_view(), {},
        name='organizer-update-homework-nocourse'),
    url(r'^update-homework/(?P<course_slug>[\d\w-]+)/$',
        UpdateHomeworkView.as_view(), {}, name='organzer-update-homework-course'),
    url(r'^(?P<slug>[\d\w-]+)/$', organizer_view, {},
        name='organizer'),
    url(r'^(?P<slug>[\d\w-]+)/(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$', organizer_view, {},
        name='organizer-date'),
    url(r'^print/(?P<slug>[\d\w-]+)/$', organizer_view, {'template_name':'organizer/organizer_print.html'},
        name='organizer-print'),
)
