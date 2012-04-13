# Create your views here.
from datetime import datetime

from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response

from schoolr.news.models import NewsMessage

class PageDetailView(DetailView):
    def get_queryset(self):
        parent_slug = self.kwargs.get('parent', None)
        return self.model._default_manager.filter(parent__slug=parent_slug)