from django.contrib import admin
from freevle.virtualcr.models import VirtualClassroom, Section

class VirtualCRAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class SectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(VirtualClassroom, VirtualCRAdmin)
admin.site.register(Section, SectionAdmin)
