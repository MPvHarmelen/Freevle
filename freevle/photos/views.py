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
		gallery_slug = self.kwargs.get('gallery', None)
		return self.model._default_manager.filter(gallery__slug=gallery_slug)
