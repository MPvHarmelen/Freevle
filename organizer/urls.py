from django.conf.urls.defaults import *
from cygy.organizer.views import UserView

from django.contrib.auth.models import User

urlpatterns = patterns('',
	url(r'^(?P<username>[\w-]+)/$', UserView.as_view(model=User),
	 name='organizer-user'),
) 