from django.contrib import admin
from freevle.virtualcr.plugins.vcr_pages.models import Page

class VCRPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Page, VCRPageAdmin)
