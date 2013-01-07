from django.conf.urls.defaults import *
from freevle.photos.views import DetailView, ListView

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(), name='album-list'),
    url(r'^(?P<slug>[-\w]*)/$', DetailView.as_view(), name='album-detail'),
#    url(r'^(?P<album>[-\w]*)#(?P<slug>[-\w]*)', )
)