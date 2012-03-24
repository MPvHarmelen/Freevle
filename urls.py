from django.conf.urls.defaults import *
from django.views.generic import TemplateView
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = []

if settings.STATIC:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

urlpatterns += patterns('',
    # Example:
    # (r'^foo/', include('cygy.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^news/', include('cygy.news.urls')),
    url(r'^letters/', include('cygy.letters.urls')),
    url(r'^galleries/', include('cygy.galleries.urls')),
    # TEMP for Floris' work.
    url(r'^courses/', TemplateView.as_view(template_name='courses/index.html')),
    url(r'^contact/', TemplateView.as_view(template_name='contact/index.html')),
    url(r'^settings/', TemplateView.as_view(template_name='settings/index.html')),
    url(r'^photos/', TemplateView.as_view(template_name='photos/index.html')),
    url(r'^course/', TemplateView.as_view(template_name='courses/wiskunde.html')),

    # User urls
    url(r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # If no url could be found, include cms:
    url('', include('cygy.cms.urls'))
)
