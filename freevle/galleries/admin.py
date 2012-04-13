from django.contrib import admin
from freevle.galleries.models import Gallery, Photo

class GalleryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	list_display = ('name','date')

class PhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title',)

admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Photo,PhotoAdmin)
