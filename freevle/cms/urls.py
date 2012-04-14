from django.conf.urls.defaults import *
from freevle.cms.views import PageDetailView

from freevle.cms.models import Page

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', PageDetailView.as_view(model=Page),
        name='cms-parent-detail'),
    url(r'^(?P<parent>[\w-]+)/(?P<slug>[\w-]+)/$',
        PageDetailView.as_view(model=Page), name='cms-child-detail'),
)
