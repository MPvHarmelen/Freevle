from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from freevle.users.views import *

urlpatterns = patterns('',
    url(r'^changepassword/$', changepassword),
    url(r'^(?P<page>\w*/?)$',
        TemplateView.as_view(template_name='user/settings.html')),
)
