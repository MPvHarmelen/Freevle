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
    # (r'^foo/', include('freevle.foo.urls')),
    url(r'^$', 'freevle.cms.views.index'),
    url(r'^news/', include('freevle.news.urls')),
    url(r'^letters/', include('freevle.letters.urls')),
    #url(r'^settings/', include('freevle.users.urls')),
    #url(r'^galleries/', include('freevle.galleries.urls')),
    url(r'^organizer/', include('freevle.organizer.urls')),

    # TEMP for Floris' and Pim's brilliant work.
    url(r'^404/', TemplateView.as_view(template_name='404.html')),
    url(r'^courses/$', TemplateView.as_view(template_name='courses/index.html')),
    url(r'^courses/grieks', TemplateView.as_view(template_name='courses/grieks.html')),
    url(r'^courses/wiskunde', TemplateView.as_view(template_name='courses/wiskunde.html')),
    url(r'^courses/duits', TemplateView.as_view(template_name='courses/duits.html')),
    url(r'^courses/upload', TemplateView.as_view(template_name='courses/uploadfile.html')),
    url(r'^contact/', TemplateView.as_view(template_name='contact/index.html')),
    url(r'^rooster/', TemplateView.as_view(template_name='rooster.html')),
    url(r'^photos/', TemplateView.as_view(template_name='photos/index.html')),
    url(r'^galleries/', TemplateView.as_view(template_name='photos/galleries.html')),
    url(r'^messages/$', TemplateView.as_view(template_name='messages/index.html')),
    url(r'^messages/new', TemplateView.as_view(template_name='messages/new.html')),
    url(r'^course/', TemplateView.as_view(template_name='courses/wiskunde.html')),
    url(r'^addhomework/', TemplateView.as_view(template_name='organizer/addhomework.html')),
    url(r'^settings/personal', TemplateView.as_view(template_name='user/personal.html')),
    url(r'^settings/changepassword', TemplateView.as_view(template_name='user/password.html')),
    url(r'^settings/coursesmenu', TemplateView.as_view(template_name='user/coursesmenu.html')),
    url(r'^profile/', TemplateView.as_view(template_name='user/profile.html')),

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
    url('', include('freevle.cms.urls'))
)
