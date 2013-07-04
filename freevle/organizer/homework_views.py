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
    # Now the day we want is at the end of the list
    all_lessons = sorted(course.lesson_set.all(), key=key)
    if len(all_lessons) == 0:
        return None, []
    lessons = []
    lesson = all_lessons.pop()
    day_of_week = None

    while lessons == [] or lesson.day_of_week == day_of_week:
        if day_of_week != lesson.day_of_week:
            day_of_week = lesson.day_of_week

            # If the distance is 0, it should be a whole week.
            days = (day_of_week - int(last_date.strftime('%w'))) % 7 or 7
            new_date = last_date + datetime.timedelta(days=days)

        if lesson.start_date <= new_date <= lesson.end_date:
            lessons.append(lesson)

        if len(all_lessons) > 0:
            lesson = all_lessons.pop()
        elif lessons == []:
            return last_date + datetime.timedelta(days=7), []
        else:
            break

    return new_date, sorted(lessons, key=lambda a:a.period)

def get_empty_homework(course, date, content='', period=None):
    '''
    Returns a Homework object without a HomeworkType. Because the HomeworkType
    is in the name of a Homework object, you can't print an 'empty' Homework.
    '''
    return Homework(
        content='',
        course=course,
        due_date=date,
        period=period
    )

@login_required
def update_homework_view(request, slug=None, days_of_the_future=60,
                         date_format='%d-%m-%Y', human_date_format='dd-mm-yyyy',
                         homework_list=None):
    if slug is None:
        raise ImproperlyConfigured('update_homework_view should be called with '
                                   'a slug.')
    # URL gives unicode, so...
    days_of_the_future = int(days_of_the_future)

    # Check if the user actually gives this course.
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
            there_are_errors = False
            for i, id in enumerate(ids):
                try:
                    periods[i] = int(periods[i])
                except ValueError:
                    periods[i] = None
                try:
                    id = int(id)
                except ValueError:
                    id = None
                try:
                    homework = Homework.objects.get(id=id)
                except Homework.DoesNotExist:
                    homework = Homework(course=course)
                else:
                    if homework.course != course:
                        # This means someone inserted an id in the html
                        # and because they aren't allowed to edit homework
                        # other than for this course:
                        raise PermissionDenied()

                homework.content = contents[i]
                homework.period = periods[i]
                homework.homework_type_id = hw_types[i]

                errors = {}
                try:
                    homework.due_date = datetime.datetime.strptime(due_dates[i], date_format).date()
                except ValueError as e:
                    errors.update(due_date=_('Date not recognised, correct format: {}'.format(human_date_format)))
                if not (homework.content == '' and homework.homework_type_id == ''):
                    try:
                        homework.full_clean()
                    except ValidationError as e:
                        for arg, messages in e.message_dict.items():
                            errors[arg] = [_(m) for m in messages]
                else:
                    # This is still an empty homework
                    homework_list.append(homework)
                    continue

                if errors == {}:
                    homework.save()
                    # This has to be verbal because the template language sucks.
                    homework.saved = 'yes'
                else:
                    there_are_errors = True
                    homework.saved = 'no'

                homework.errors = errors
                homework_list.append(homework)

            # Then check where to go.
            if there_are_errors:
                # Render the same page again
                pass
            else:
                course_slug = request.POST.get('course') or course.slug
                url = 'organizer-update-homework'
                kwargs = {'slug': course_slug}
                return HttpResponseRedirect(reverse(url, kwargs=kwargs))

        else:
            if homework_list is None:
                # get_next_lessons only does dates AFTER `date`, so `date` must
                # be yesterday to include today.
                date = datetime.date.today() - datetime.timedelta(days=1)
                end_date = date + datetime.timedelta(days=days_of_the_future)
                homework = course.homework_set.filter(due_date__gt=date,
                                                      due_date__lte=end_date)
                homework_list = list(homework)
                date, lessons = get_next_lessons(course, date)
                if date is None:
                    # This means there are no lessons for this course
                    date = end_date
                while date < end_date:
                    for lesson in lessons:
                        if len(homework.filter(due_date=date, period=lesson.period)) == 0:
                            empty_homework = get_empty_homework(course, date, period=lesson.period)
                            homework_list.append(empty_homework)
                    date, lessons = get_next_lessons(course, date)
                homework_list.sort(key=lambda a: (a.due_date, a.period))
    else:
        raise PermissionDenied(_('You need to give the course {} to acces this '
                                 'page.'.format(course)))

    # Template variables
    homework_types = HomeworkType.objects.all()
    courses = sorted(request.user.gives_courses.all(), key=lambda a: a.name)
    url = 'organizer-update-homework-date'
    kwargs = {'slug' : course.slug,
              'days_of_the_future': days_of_the_future + 10}
    more_url = reverse(url, kwargs=kwargs)
    return render(request,
                  'organizer/homework_form.html',
                  {'homework_list': homework_list,
                   'homework_types': homework_types,
                   'course': course,
                   'courses': courses,
                   'more_url': more_url})
