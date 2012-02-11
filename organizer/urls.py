from django.conf.urls.defaults import *
from cygy.organizer.views import UserView

from django.contrib.auth.models import User

urlpatterns = patterns('',
	url(r'^(?P<username>[\w-]+)/$', UserView.as_view(template_name='organizer/my_schedule.html'),
	 	name='organizer-user'),
	url(r'^(?P<username>[\w-]+)/(?P<day>\d{2})/(?P<month>\d{2})/$', UserView.as_view(template_name='organizer/my_schedule.html'),
	 	name='organizer-user-day'),
) 