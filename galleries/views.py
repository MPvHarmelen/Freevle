# Create your views here.
from django.views.generic.detail import DetailView

class GalleryDetailView(DetailView):
	def get_queryset(self):
		gallery_slug = self.kwargs.get('gallery', None)
		return self.model._default_manager.filter(gallery__slug=gallery_slug)
