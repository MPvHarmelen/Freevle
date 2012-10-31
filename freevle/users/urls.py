from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from freevle.users.views import *

urlpatterns = patterns('',
    url(r'^(?:personal)?/$', changepassword),
    url(r'^changepassword/$', changepassword),
    url(r'^virtualcrs/$', changepassword),
)
