from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView

from freevle.virtualcr import plugins, views

urls = ['']

# Include urls for plugins
for plugin in plugins.get_plugins():
    urls.append(url(r'^(?P<slug>[-\w]*)/' + plugin[0] + '/', include(plugin[1] + '.urls')))

urls.append(
        url(r'^(?P<slug>[-\w]*)/$', views.VirtualCRView.as_view(),
            name='virtualcr-detail')
    )

urlpatterns = patterns(*urls)
