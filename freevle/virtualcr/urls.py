from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView

from freevle.virtualcr.models import VirtualClassroom

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]*)', DetailView.as_view(
            model=VirtualClassroom,
            context_object_name='virtualcr'
        ),
        name='virtualcr-detail')
)

