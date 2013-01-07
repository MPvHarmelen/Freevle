from django.contrib import admin
from freevle.virtualcr.plugins.vcr_files.models import File

class VCRFileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(File, VCRFileAdmin)
