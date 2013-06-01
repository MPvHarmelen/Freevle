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
from django.core.exceptions import PermissionDenied, ValidationError

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


def get_next_lessons(course, last_date):
    '''
    Returns an orderd list of all the lessons on the next day a lesson occurs
    and the date: (date, list)
    '''
    homework = None
    # This key gives the day after last_date the highest score, the day after
    # one point lower and last_date itself the lowest.
    key = lambda a: (int(last_date.strftime('%w')) - a.day_of_week) % 7
    # Now the day we want is at the beginning of the list
    all_lessons = sorted(course.lesson_set.all(), key=key, reverse=True)
    if len(all_lessons) < 1:
        raise ImproperlyConfigured('There are no lessons for {}'.format(course))
    lessons = []
    day_of_week = all_lessons[0].day_of_week
    for lesson in all_lessons:
        if lesson.day_of_week == day_of_week:
            lessons.append(lesson)
        else:
            # Because the list is sorted, we can stop the loop the first time
            # we encounter a lesson that's not on the right day.
            break
    # If the distance is 0, it should be a whole week.
    days = (day_of_week - int(last_date.strftime('%w'))) % 7 or 7
    new_date = last_date + datetime.timedelta(days=days)

    return new_date, sorted(lessons, key=lambda a:a.period)

def get_empty_homework(course, date, content='', period=None):
    '''
    Returns a Homework object without a HomeworkType. Because the HomeworkType
    is in the name of a Homework object, you can't an 'empty' Homework.
    '''
    return Homework(
        content='',
        course=course,
        due_date=date,
        period=period
    )

@login_required
def update_homework_view(request, slug=None, minimum_homework=10, date_format='%d-%m-%Y', homework_list=None):
    if slug is None:
        raise ImproperlyConfigured('update_homework_view should be called with '
                                   'a slug.')
    # check if the user actually gives this course.
    course = Course.objects.get(slug=slug)
    if course in request.user.gives_courses.all():
        if request.method == 'POST':
            # First save and validate all that shit.
            ids = request.POST.getlist('id')
            hw_types = request.POST.getlist('homework_type')
            contents = request.POST.getlist('content')
            due_dates = request.POST.getlist('due_date')
            periods = request.POST.getlist('period')
            homework_list = []
            due_dateles_homework_list = []
            for i, id in enumerate(ids):
                if periods[i] == 'None':
                    periods[i] = None
                if id == 'None':
                    id = None
                try:
                    homework = Homework.objects.get(id=id)
                except Homework.DoesNotExist:
                    homework = Homework(course=course)
                else:
                    if homework.course != course:
                        # This means someone inserted an id in the html
                        # and because they aren't allowed to edit other
                        # homework than for this course:
                        raise PermissionDenied()

                homework.content = contents[i]
                homework.period = periods[i]
                homework.homework_type_id = id=hw_types[i]

                errors = {}
                try:
                    homework.due_date = datetime.datetime.strptime(due_dates[i], date_format).date()
                except ValueError as e:
                    errors.update(due_date=_('Date not recognised, correct format: {}'.format(date_format)))

                try:
                    homework.full_clean()
                except ValidationError as e:
                    for arg, messages in e.message_dict.items():
                        errors[arg] = [_(m) for m in messages]

                if errors == {}:
                    homework.save()
                    print 'saved'
                    # This has to be verbal because the template language sucks.
                    homework.saved = 'yes'
                else:
                    homework.saved = 'no'

                homework.errors = errors
                homework_list.append(homework)

            # This has to be fed to the template or something...
            homework_list.sort(key=lambda a: (a.due_date, a.period))

            # Then check where to go.
            course_slug = request.POST.get('course') or course.slug
            url = 'organizer-update-homework'
            kwargs = {'slug':course_slug}
            return HttpResponseRedirect(reverse(url, kwargs=kwargs))

        else:
            if homework_list is None:
                homework_list = []
                # get_next_lessons only does dates AFTER `date`, so `date` must be
                # yesterday to include today.
                prev_date = datetime.date.today() - datetime.timedelta(days=1)
                while len(homework_list) < minimum_homework:
                    date, lessons = get_next_lessons(course, prev_date)
                    homework = course.homework_set.filter(
                        due_date__gt=prev_date,
                        due_date__lte=date
                    )
                    homework_list.extend(homework)
                    for lesson in lessons:
                        if len(homework.filter(due_date=date, period=lesson.period)) == 0:
                            homework_list.append(get_empty_homework(course, date, period=lesson.period))
                    prev_date = date
                homework_list.sort(key=lambda a: (a.due_date, a.period))

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

