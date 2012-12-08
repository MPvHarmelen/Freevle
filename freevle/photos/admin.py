from django.contrib import admin
from freevle.photos.models import Album, Photo

class AlbumAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	list_display = ('name', 'creation_date')

class PhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'album')

admin.site.register(Album,AlbumAdmin)
admin.site.register(Photo,PhotoAdmin)
