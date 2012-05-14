import datetime

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from freevle.organizer.models import *

# You have to be careful with EmptyLesson, because empty
# ForeignKey fields raise DoesNotExist.

class StrCourse(Course):
    topic = str()

class DateMixin(object):
    year = None
    month = None
    day = None

    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'

    allow_weekend = False
    number_days = 3

    def get_number_days(self):
        return self.number_days

    ## Edited
    def get_year(self):
        """
        Return the year for which this view should display data
        """
        year = self.year
        if year is None:
            try:
                year = self.kwargs['year']
            except KeyError:
                year = datetime.date.today().year
        return str(year)

    ## Edited
    def get_month(self):
        """
        Return the month for which this view should display data
        """
        month = self.month
        if month is None:
            try:
                month = self.kwargs['month']
            except KeyError:
                month = datetime.date.today().month
        return str(month)

    ## Edited
    def get_day(self):
        """
        Return the day for which this view should display data
        """
        day = self.day
        if day is None:
            try:
                day = self.kwargs['day']
            except KeyError:
                day = datetime.date.today().day
        return str(day)

    def get_year_format(self):
        """
        Get a year format string in strptime syntax to be used to parse the
        year from url variables
        """
        return self.year_format

    def get_month_format(self):
        """
        Get a month format string in strptime syntax to be used to parse the
        month from url variables
        """
        return self.month_format

    def get_day_format(self):
        """
        Get a day format string in strptime syntax to be used to parse the
        day from url variables
        """
        return self.day_format

    def get_allow_weekend(self):
        """
        Return if a date is allowed to be a Saturday or Sunday.
        """
        return self.allow_weekend

    def check_allow_weekend(self, date):
        """
        Check if a date is allowd to be a Saturday or Sunday,
        return a date that isn't a Saturday or Sonday if it isn't allowd to be
        """
        allow_weekend = self.get_allow_weekend()

        if not allow_weekend:
            if date.strftime('%a') == 'Sat':
                date += datetime.timedelta(days=2)
            elif date.strftime('%a') == 'Sun':
                date += datetime.timedelta(days=1)

        return date

    def get_date(self):
        """
        Return the date for which this view should display data
        """
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()

        year_format = self.get_year_format()
        month_format = self.get_month_format()
        day_format = self.get_day_format()

        delim = '__'

        date_format = delim.join((year_format, month_format, day_format))
        date_string = delim.join((year, month, day))

        date = datetime.datetime.strptime(date_string, date_format).date()
        date = self.check_allow_weekend(date)

        return date


class CancellationMixin(object):
    def check_cancellation(self, lesson_list):
        for lesson in lesson_list:
            # do stuff
            pass

        return lesson_list

class HomeworkMixin(object):
    comming_homework_days = 14
    comming_homework_min_weight = 10
    coming_homework = None

    def set_homework(self, lesson_set, date):
        key = lambda a: a.homework_type.weight
        for lesson in lesson_set:
            lesson.homework = sorted(
                [homework for homework in lesson.homework_set.filter(
                    due_date=date
                 )],
                key=key,
                # A higher weight is more important & more important homework
                # should go first, thus:
                reverse=True
            )
        return lesson_set

    def get_coming_homework(self, date, user):
        coming_homework = self.coming_homework
        min_weight = self.comming_homework_min_weight

        if coming_homework is None:
            comming_homework = []
            days = self.comming_homework_days
            for course in user.takes_courses.all():
                for lesson in course.lesson_set.all():
                    end_date = date + datetime.timedelta(days=days)
                    comming_homework.extend(
                        lesson.homework_set.filter(
                            due_date__gt=date,
                            due_date__lt=end_date,
                            homework_type__weight__gt=min_weight
                        )
                    )

        return coming_homework

    def set_homework(self, lesson_set, date):
        key = lambda a: a.homework_type.weight
        for lesson in lesson_set:
            lesson.homework = sorted(
                [homework for homework in lesson.homework_set.all() if
                 homework.due_date == date],
                 key=key,
                 # Higher weights is more important & more important homework
                 # should go first, thus:
                 reverse=True
            )
        return lesson_set

class LessonListMixin(DateMixin):
    lesson_lists = None
    empty_lesson_tekst = '-'

    def get_min_periods(self, date):
        periodmeta = PeriodMeta().get_periodmeta(date)
        return periodmeta.min_periods

    def set_period_times(self, lesson_list, date):
        '''
        Get the right times for periods
        '''
        periodmeta = PeriodMeta().get_periodmeta(date)
        latest_period = lesson_list[-1].period
        period_times = periodmeta.get_period_times(latest_period)

        for index, time in enumerate(period_times):
            start_hour = str(time[0].hour).rjust(2,'0')
            start_minute = str(time[0].minute).rjust(2,'0')
            end_hour = str(time[1].hour).rjust(2,'0')
            end_minute = str(time[1].minute).rjust(2,'0')

            lesson_list[index].start_time = start_hour + ':' + start_minute
            lesson_list[index].end_time = end_hour + ':' + end_minute

        return lesson_list

    def get_lesson_set(self, date):
        '''
        Returns an iterable of lessons for the given date and object.
        '''
        raise ImproperlyConfigured('You must write your own `get_lesson_set`')

    def get_lesson_lists(self, date, obj):
        """
        Get the list of lessonsets. This is a list of iterables.
        """
        if self.lesson_lists is not None:
            lesson_lists = self.lesson_lists
        else:
            number_days = self.get_number_days()

            date_list = []
            for n in range(number_days):
                if n == 0:
                    list_date = date
                else:
                    list_date = date_list[-1] + datetime.timedelta(days=1)
                    list_date = self.check_allow_weekend(list_date)

                date_list.append(list_date)

            sort = lambda a: sorted(a, key=lambda b: b.period)
            lesson_lists = [sort(self.get_lesson_set(date_list[n], obj))
                            for n in range(number_days)]

            # For loop to get the length for lesson_set_cleanup
            length = 0
            for index, lesson_set in enumerate(lesson_lists):
                if len(lesson_set) != 0:
                    latest_period = lesson_set[-1].period
                    list_date = date_list[index]
                    min_period = self.get_min_periods(list_date)

                    if latest_period > length:
                        length = latest_period
                    if min_period > length:
                        length = min_period

            for index, lesson_set in enumerate(lesson_lists):
                date = date_list[index]
                lesson_set = self.lesson_set_cleanup(lesson_set, length, date)
                try:
                    lesson_set = self.set_homework(lesson_set, date)
                except AttributeError:
                    # The Homework mixin isn't required
                    pass
                lesson_set = self.check_cancellation(lesson_set)

        return lesson_lists

    def lesson_set_cleanup(self, lesson_set, min_length, date):
        """
        Takes an iterable of lessons, returns a lesson_list ready to be
        itterated for the template. (No cancellation is checked)
        """
        empty_course = StrCourse(topic=self.empty_lesson_tekst)
        empty_lesson = lambda: Lesson(course=empty_course)

        unpadded_list = list(lesson_set)
        unpadded_list.sort(key=lambda a: a.period)

        lesson_list = []
        for index, lesson in enumerate(unpadded_list):
            if index == 0:
                previous_period = 0
            else:
                # Get the period of the previous lesson in unpadded_list
                previous_period = unpadded_list[index - 1].period

            # Check if this period is directly after the previous one
            if lesson.period != previous_period + 1:
                difference = lesson.period - previous_period
                # Two adjacent hours differ 1
                lesson_list.extend((empty_lesson() for i in range(difference - 1)))

            lesson_list.append(lesson)

        # Correct length
        length = len(lesson_list)
        if length < min_length:
            lesson_list.extend((empty_lesson() for i in range(min_length - length)))

        if len(lesson_list) > 0:
            lesson_list = self.set_period_times(lesson_list, date)

        days_dict = dict(DAY_CHOICES)
        # Set day_of_week to full regional name
        for lesson in lesson_list:
            try:
                lesson.day_of_week = day_of_week = days_dict[lesson.day_of_week]
            except KeyError:
                try:
                    lesson.day_of_week = day_of_week
                except UnboundLocalError:
                    # This should be done differently
                    pass

        return lesson_list

class OrganizerView(View, CancellationMixin, LessonListMixin):
    template_name = None
    response_class = TemplateResponse
    announcements = None

    def get_announcements(self, date):
        announcements = self.announcements
        if announcements is None:
            announcements = Announcements.objects.filter(
                start_date__lt=date,
                end_date__gt=date
            )

        return announcements

    def get_legend(self):
        return HomeworkType.objects.all()

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]


    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self):
        """
        Get the context for this view.
        """
        date = self.get_date()
        user = self.get_user()
        announcements = self.get_announcements(date)
        coming_homework = self.get_coming_homework(date, user)
        lesson_lists = self.get_lesson_lists(date, user)
        legend = self.get_legend()

        context = {
            'announcements': announcements,
            'coming_homework': coming_homework,
            'lesson_lists': lesson_lists,
            'legend': legend,
        }
        return context



class StudentView(OrganizerView, HomeworkMixin):
    """
    To write:
    class CancellationMixin
        check_cancellation(lesson)
    """
    username_url_kwarg = 'username'
    user = None

    def get_user(self):
        username = self.kwargs.get(self.username_url_kwarg, None)

        if self.user is not None:
            return self.user
        elif username is not None:
            try:
                user = User.objects.get(username=username,
                                        groups__name='students')
            except ObjectDoesNotExist:
                raise Http404("This user doesn't exist")
        else:
            raise ImproperlyConfigured("StudentView should be called with "
                                       "a user or username")
        return user

    ## Home Made
    def get_lesson_set(self, date, user):
        """
        Returns a list of lessons for the given user and date,
        ordered by period
        """

        day_of_week = date.strftime('%a')
        lesson_list = []
        for course in user.takes_courses.all():
            lesson_subset = course.lesson_set.filter(
                day_of_week=day_of_week,
                start_date__lt=date,
                end_date__gt=date
            )
            lesson_list.extend(lesson_subset)
        return lesson_list

def organizer_view(request, **kwargs):
    slug = kwargs.pop('slug', None)
    if slug is not None:
        try:
            user = User.objects.get(username=slug)
            if 'students' in (group.name for group in user.groups.all()):
                # Twice giving **kwargs is ugly, but it works :(
                return StudentView.as_view(user=user, **kwargs)(request, **kwargs)
            elif 'teachers' in (group.name for group in user.groups.all()):
                raise KeyError('Teacher')
            else:
                raise Http404("Couldn't find organizer data for this slug.")
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

