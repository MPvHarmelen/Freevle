from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^(?P<page>\w*/?)$', TemplateView.as_view(template_name='user/settings/index.html')),
)

