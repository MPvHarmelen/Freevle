from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list

from cygy.cms.models import Page

urlpatterns = patterns('',
    (r'^$', object_list, {'queryset': Page.objects.all(), 'template_object_name':'Page'}),
    (r'^(?P<slug>[\w-]+)/$', object_detail, {'queryset': Page.objects.all(), 'template_object_name':'Page'}),
)
