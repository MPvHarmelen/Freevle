from django.contrib import admin
from freevle.virtualcr.models import VirtualClassroom, Section, Attachment

class VirtualCRAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class EmptyAdmin(admin.ModelAdmin):
    pass

admin.site.register(VirtualClassroom, VirtualCRAdmin)
admin.site.register(Section, EmptyAdmin)
admin.site.register(Attachment, EmptyAdmin)
