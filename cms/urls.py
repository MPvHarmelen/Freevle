from django.conf.urls.defaults import *
from cygy.cms.views import PageView
from django.views.generic.list_detail import object_list

from cygy.cms.models import Page

urlpatterns = patterns('',
    (r'^$', object_list, {'queryset': Page.objects.all(), 'template_object_name':'Page'}),
    (r'^(?P<parent>[\w-]+)/(?P<slug>[\w-]+)/$', PageView.as_view(model=Page)),
)
