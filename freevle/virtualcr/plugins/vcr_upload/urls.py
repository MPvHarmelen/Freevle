from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from freevle.virtualcr.plugins.vcr_upload.models import Assignment

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]*)/$',
        DetailView.as_view(model=File, context_object_name='assignment'),
        name='virtualcr-upload-detail')
)


def get_url_root():
    return 'upload/'
