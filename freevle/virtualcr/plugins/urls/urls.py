from django.conf.urls import *
from django.views.generic.detail import DetailView
from .models import UrlsPlugin

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]*)/$', DetailView.as_view(model=UrlsPlugin),
        name='urlsplugin-detail')
#    url(r'^(?P<gallery>[-\w]*)#(?P<slug>[-\w]*)', )
)
