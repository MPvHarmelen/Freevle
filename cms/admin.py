from django.contrib import admin
from cygy.cms.models import Page

class PageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Page,PageAdmin)
