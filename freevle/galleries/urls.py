from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView

from freevle.galleries.models import Gallery

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]*)$', DetailView.as_view(model=Gallery),
        name='gallery-detail')
#    url(r'^(?P<gallery>[-\w]*)#(?P<slug>[-\w]*)', )
)