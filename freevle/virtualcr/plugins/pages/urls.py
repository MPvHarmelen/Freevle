from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from freevle.virtualcr.plugins.pages.models import Page

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]*)/$',
        DetailView.as_view(model=Page, context_object_name='page'),
        name='virtualcr-page-detail')
)


def get_url_root():
    return 'page/'