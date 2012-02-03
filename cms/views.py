# Create your views here.
from django.views.generic.detail import DetailView

class PageView(DetailView):
    def get_queryset(self):
        parent = self.kwargs.get('parent', None)
        return self.model._default_manager.filter(parent__slug=parent)
