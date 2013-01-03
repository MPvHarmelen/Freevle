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

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from freevle.organizer.forms import HomeworkForm

class HomeworkUpdate(UpdateView):
    template_name = 'organizer/add_homework.html'
    form_class = HomeworkForm

class HomeworkCreate(CreateView):
    model = Homework
    course_slug = None


class HomeworkView(FormView):
    template_name = 'organizer/homework_form.html'
    form_class = HomeworkForm
    succes_url = '/organizer/'

    def get_context_data(self, **kwargs):
        return super(HomeworkView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        # bla bla

        # The below just redirects to succes_url
        return super(AddHomeworkView, self).form_valid(form)
