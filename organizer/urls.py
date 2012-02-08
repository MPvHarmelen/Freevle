from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User

urlpatterns = patterns('',
	url(r'^(?P<username>[\w-]+)/$', DetailView.as_view(model=User),
	 name='organizer-user'),
) 