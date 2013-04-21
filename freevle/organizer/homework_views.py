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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

@login_required
def get_course_view(request):
    if request.user.groups.filter(name='teachers'):
        if request.method == 'POST':
            url = 'organizer-update-homework'
            warnings.warn('\n\t Is this safe?\n')
            kwargs = {'slug':request.POST['course']}
            return HttpResponseRedirect(reverse(url, kwargs=kwargs))
        else:
            courses = sorted(request.user.gives_courses.all(),
                             key=lambda a: a.name)
            return render(request,
                          'organizer/course_form.html',
                          {'courses':courses})
    else:
        raise PermissionDenied(_('You need to be a teacher to acces this page.'))

@login_required
def update_homework_view(request, slug=None):
    if slug is None:
        raise ImproperlyConfigured('update_homework_view should be called with '
                                   'a slug.')
    # check if the user actually gives this course.
    course = Course.objects.get(slug=slug)
    if course in request.user.gives_courses.all():
        if request.method == 'POST':
            # First save and validate all that shit.
            pass

            # Then check where to go.
            course = request.POST.get('course')
            if course is not None:
                url = 'organizer-update-homework'
                warnings.warn('\n\t Is this safe?\n')
                kwargs = {'slug':request.POST['course']}
                return HttpResponseRedirect(reverse(url, kwargs=kwargs))

        else:
            homework_list = []
            # Build list of current homework
            today = datetime.date.today()

            for lesson in course.lesson_set.all():
                homework_list.extend(lesson.homework_set.all())

            homework_list.sort(key=lambda a: a.due_date)


            # Template variables
            homework_types = HomeworkType.objects.all()

            courses = sorted(request.user.gives_courses.all(),
                             key=lambda a: a.name)
            return render(request,
                          'organizer/homework_form.html',
                          {'homework_list':homework_list,
                           'homework_types':homework_types,
                           'course':course,
                           'courses':courses})
    else:
        raise PermissionDenied(_('You need to give the course {} to acces this '
                                 'page.'.format(course)))
@login_required
def update_homework_extend(request):
    pass

