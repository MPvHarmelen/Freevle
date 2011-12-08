from django.contrib import admin
from cygy.cms.models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', )


admin.site.register(Page,PageAdmin)
