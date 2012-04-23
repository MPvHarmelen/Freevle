from django.conf.urls.defaults import *
from freevle.organizer.views import StudentView

urlpatterns = patterns('',
    url(r'^(?P<username>[\d\w-]+)/$', StudentView.as_view(template_name='organizer/my_schedule.html'),
        name='organizer-user'),
    url(r'^(?P<username>[\d\w-]+)/(?P<day>\d{2})/(?P<month>\d{2})/$', StudentView.as_view(template_name='organizer/my_schedule.html'),
        name='organizer-user-day'),
) 
