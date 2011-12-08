from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from cygy.cms.models import Page

urlpatterns = patterns('',
    (r'(P?<slug>\d+)', object_detail, {'queryset': Page.objects.all(),
                                          'slug': '%(slug)s'
     }))
