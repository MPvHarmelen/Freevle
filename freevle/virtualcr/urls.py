from django.conf.urls.defaults import *

from freevle.virtualcr import plugins, views

urls = ['']

# Include urls for plugins
for plugin in plugins.get_plugin_urls():
    urls.append(url(r'^(?P<vcr_slug>[-\w]*)/' + plugin[0] , include(plugin[1] + '.urls')))

urls.append(
        url(r'^(?P<vcr_slug>[-\w]*)/$', views.VirtualCRView.as_view(),
            name='virtualcr-detail')
    )

urlpatterns = patterns(*urls)
