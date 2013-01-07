# Create your views here.
from django.views.generic.detail import DetailView as GenericDetail
from django.views.generic import ListView as GenericList
from freevle.photos.models import Album

class ListView(GenericList):
    model = Album

class DetailView(GenericDetail):
    model = Album

class PhotoDetailView(DetailView):
	def get_queryset(self):
		album_slug = self.kwargs.get('album', None)
		return self.model._default_manager.filter(album__slug=album_slug)
