from django.contrib import admin
from cygy.cms.models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Page,PageAdmin)
