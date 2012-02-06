from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView

from cygy.galleries.models import Gallery

urlpatterns = patterns('',
	url(r'^(?P<gallery>[-\w]*)', DetailView.as_view(model=Gallery), name='gallery-detail')
)