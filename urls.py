from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
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
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^news/', include('cygy.news.urls')),
    url(r'^letters/', include('cygy.letters.urls')),
    url(r'^galleries/', include('cygy.galleries.urls')),
    url(r'^organizer/', include('cygy.organizer.urls')),

    # TEMP for Floris' work.
    url(r'^courses/', direct_to_template, {'template': 'courses/index.html'}),
    url(r'^contact/', direct_to_template, {'template': 'contact/index.html'}),


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
