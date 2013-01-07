from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from freevle.virtualcr.plugins.vcr_files.models import File

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]*)/$',
        DetailView.as_view(model=File, context_object_name='page'),
        name='virtualcr-file-detail')
)


def get_url_root():
    return 'file/'
