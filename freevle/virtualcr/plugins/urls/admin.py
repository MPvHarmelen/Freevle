from django.contrib import admin
from freevle.virtualcr.plugins.urls.models import UrlsPlugin

class UrlsPluginAdmin(admin.ModelAdmin):
    pass

admin.site.register(UrlsPlugin, UrlsPluginAdmin)
