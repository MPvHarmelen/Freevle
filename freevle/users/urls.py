from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from freevle.users.views import *

urlpatterns = patterns('',
    url(r'^changepassword/$', changepassword),
    url(r'^virtualcrs/$', TemplateView.as_view(
                              template_name='users/virtualcr_list.html')),
    url(r'^(personal/)?$', ProfileUpdateView.as_view()),
)
