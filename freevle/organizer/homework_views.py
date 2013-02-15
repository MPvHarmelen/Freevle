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
from freevle.organizer.views import *
# The above is already there in organier.views

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from freevle.organizer.forms import HomeworkForm, HCourseForm

class HomeworkUpdate(UpdateView):
    template_name = 'organizer/add_homework.html'
    form_class = HomeworkForm

class HomeworkCreate(CreateView):
    model = Homework
    course_slug = None

class TeacherProtectionMixin(FormView):
    permission = ''
    @method_decorator(permission_required(permission))
    def dispatch(self, *args, **kwargs):
        return super(TeacherProtectionMixin, self).dispatch(*args, **kwargs)


class GetCourseView(FormView):
    template_name = 'organizer/course_form.html'
    form_class = HCourseForm
    succes_url = '/organizer/'

    def form_valid(self, form):
        url = 'organzer-update-homework'
        kwargs = {'course_slug':form.data['course'].slug}
        return HttpResponseRedirect(reverse(url, kwargs=kwargs))


class UpdateHomeworkView(FormView):
    template_name = 'organizer/homework_form.html'
    form_class = HomeworkForm
    succes_url = '/organizer/'
    course = None
    course_slug = None

    def get_course(self):
        '''Returns the course this view was called with.'''
        if self.course is not None:
            return self.course
        elif self.course_slug is not None:
            return Course.objects.get(slug=self.course_slug)
        raise ImproperlyConfigured('HomeworkView must be called with a course'
                                   'or course slug')

    def get_context_data(self, **kwargs):
        return super(UpdateHomeworkView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        # bla bla

        # The below just redirects to succes_url
        return super(AddHomeworkView, self).form_valid(form)
