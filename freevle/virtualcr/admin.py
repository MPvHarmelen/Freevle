from django.contrib import admin
from freevle.virtualcr.models import VirtualClassroom, Section, Attachment

class AttachmentInline(admin.StackedInline):
    model = Attachment

class SectionAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]

class VirtualCRAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(VirtualClassroom, VirtualCRAdmin)
admin.site.register(Section, SectionAdmin)
