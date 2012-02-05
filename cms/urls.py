from django.conf.urls.defaults import *
from cygy.cms.views import PageDetailView

from cygy.cms.models import Page

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', PageDetailView.as_view(model=Page),
     name='cms-parent-detail'),
    url(r'^(?P<parent>[\w-]+)/(?P<slug>[\w-]+)/$',
     PageDetailView.as_view(model=Page), name='cms-child-detail'),
)
