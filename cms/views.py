# Create your views here.
from django.views.generic.detail import DetailView

class PageDetailView(DetailView):
    def get_queryset(self):
        parent_slug = self.kwargs.get('parent', None)
        return self.model._default_manager.filter(parent__slug=parent_slug)
