from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView

from freevle.virtualcr.models import VirtualClassroom
from freevle.virtualcr import plugins

urls = ['']

# Include urls for plugins
for plugin in plugins.get_plugins():
    urls.append(url(r'^' + plugin[0] + '/', include(plugin[1] + '.urls')))

urls.append(
        url(r'^(?P<slug>[-\w]*)', DetailView.as_view(
                model=VirtualClassroom,
                context_object_name='virtualcr'
            ),
            name='virtualcr-detail')
    )

urlpatterns = patterns(*urls)
