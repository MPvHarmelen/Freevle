from django.contrib import admin
from freevle.cms.models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent',)


admin.site.register(Page,PageAdmin)
