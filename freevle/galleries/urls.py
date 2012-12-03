from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from freevle.galleries.models import Gallery

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Gallery), name='gallery-list'),
    url(r'^(?P<slug>[-\w]*)/$', DetailView.as_view(model=Gallery),
        name='gallery-detail'),
#    url(r'^(?P<gallery>[-\w]*)#(?P<slug>[-\w]*)', )
)