# Create your views here.
from django.views.generic.detail import DetailView

def PageView(DetailView):
    def get_queryset(self):
        return self.model._default_manager.all()
