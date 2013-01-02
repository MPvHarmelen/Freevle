# Just a quiet place to work
# The below is already there in organizer.views I'll delete it when moving back.
import datetime
import warnings
import copy

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from freevle.organizer.models import *
# The above is already there in organier.views

from django.views.genereic.edit import CreateView, UpdateView, DeleteView


class HomeworkUpdate(UpdateView):
    template_name = 'organizer/add_homework.html'
    form_class = HomeworkForm
    # succes_url =

    def get_context_data(self, **kwargs):
        pass

    def form_valid(self, form):
        # bla bla

        # The below just redirects to succes_url
        return super(AddHomeworkView, self).form_valid(form)
