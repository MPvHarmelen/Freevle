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
    # (r'^foo/', include('schoolr.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^news/', include('schoolr.news.urls')),
    url(r'^letters/', include('schoolr.letters.urls')),
    url(r'^galleries/', include('schoolr.galleries.urls')),
    # TEMP for Floris' and Pim's brilliant work.
    url(r'^404/', TemplateView.as_view(template_name='404.html')),
    url(r'^courses/', TemplateView.as_view(template_name='courses/index.html')),
    url(r'^contact/', TemplateView.as_view(template_name='contact/index.html')),
    url(r'^settings/$', TemplateView.as_view(template_name='settings/index.html')),
    url(r'^settings/contact/', TemplateView.as_view(template_name='settings/contact.html')),
    url(r'^settings/password/', TemplateView.as_view(template_name='settings/password.html')),
    url(r'^settings/notifications/', TemplateView.as_view(template_name='settings/notifications.html')),
    url(r'^photos/', TemplateView.as_view(template_name='photos/index.html')),
    url(r'^course/', TemplateView.as_view(template_name='courses/wiskunde.html')),

    # User urls
    url(r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'user/logout.html'}),

    url(r'^user/lostandfound/$', 'django.contrib.auth.views.logout', {'template_name': 'user/lostandfound.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # If no url could be found, include cms:
    url('', include('schoolr.cms.urls'))
)
