from django.conf.urls.defaults import *
from freevle.organizer.views import organizer_view, organizer_print_view
from freevle.organizer.homework_views import get_course_view, update_homework_view

urlpatterns = patterns('',
#    url(r'^homework-create/$', HomeworkCreate.as_view(), {},
#        name='homework-create'),
    url(r'^update-homework/$', get_course_view, {},
        name='organizer-update-homework-course'),
    url(r'^update-homework/(?P<slug>[\d\w-]+)/$', update_homework_view, {},
        name='organizer-update-homework'),
#    url(r'^update-homework/(?P<course_slug>[\d\w-]+)/$',
#        UpdateHomeworkView.as_view(), {}, name='organzer-update-homework-course'),
    url(r'^print/(?P<slug>[\d\w-]+)/$', organizer_print_view, {'template_name':'organizer/organizer_print.html'},
        name='organizer-print'),
    url(r'^(?P<slug>[\d\w-]+)/$', organizer_view, {},
        name='organizer'),
    url(r'^(?P<slug>[\d\w-]+)/(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$', organizer_view, {},
        name='organizer-date'),
)
