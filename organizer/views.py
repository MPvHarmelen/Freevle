# Create your views here.

import datetime

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _

from cygy.custom.classes import sortable_list

from django.contrib.auth.models import User
from cygy.organizer.models import Lesson, Course, PeriodLengths, DAY_CHOICES

# You have to be careful with Empty- and BreakLesson, because empty
# ForeignKey fields raise DoesNotExist.
class EmptyLesson(Lesson):
    course = Course(topic='-')

class BreakLesson(Lesson):
    course = Course(topic=_('break'))
    is_break = True


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
        return year

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
        return month

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
        return day

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
            if date.strftime('%a') is 'Sat':
                date += datetime.timedelta(days=2)
            elif date.strftime('%a') is 'Sun':
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

        return date


class CancellationMixin(object):
    def check_cancellation(self, lesson_list):
        for lesson in lesson_list:
            # do stuff
            pass

        return lesson_list

class LessonListMixin(object):
    lesson_lists = None

    def set_breaks_and_period_times(self, lesson_list, date):
        '''
        get the right times and breaks

        put them in lesson_list
        return lesson_list
        '''
        periodlengths = PeriodLengths().get_periodlengths(date)
        
        
        for index, lesson in enumerate(lesson_list[:]):
            period = index + 1
            if periodlengths.is_next_period_break(period):
                break_lesson = BreakLesson(period=period)
                break_lesson.period = period
                lesson_list[index:index] = break_lesson
                
        
        
        
        
        return lesson_list
    
    def get_lesson_set(self, date):
        '''
        Returns an iterable of lessons for the given date and object.
        '''
        raise ImproperlyConfigured('You must write your own get_lesson_set')

    def get_lesson_lists(self, date):
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
                    list_date = check_allow_weekend(list_date)
                
                date_list.append(list_date)
                
            sort = lambda a: sortable_list(a).sorted(key=lambda b: b.period)
            lesson_lists = [sort(self.get_lesson_set(date_list[n]))
                            for n in range(number_days)]
            
            # For loop to get the length for lesson_set_cleanup
            length = 0
            for index, lesson_set in enumerate(lesson_lists):
                latest_period = lesson_set[-1].period
                list_date = date_list[index]
                min_period = self.get_periods_in_day(list_date)
                
                if latest_period > length:
                    length = latest_period
                if min_period > length:
                    length = min_period
                    
            for index, lesson_set in enumerate(lesson_lists):
                date = date_list[index]
                lesson_set = self.lesson_set_cleanup(lesson_set, length, date)
                lesson_set = self.check_cancellation(lesson_set)
        
        return lesson_lists
        
    def lesson_set_cleanup(self, lesson_set, min_length, date):
        """
        Takes an iterable of lessons, returns a lesson_list ready to be
        itterated for the template. (No cancellation is checked)
        """
        empty_lesson = EmptyLesson()

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
                lesson_list.extend([empty_lesson] * (difference - 1))

            lesson_list.append(lesson)
        
        # Correct length
        length = len(lesson_list)
        if length < min_length:
            lesson_list.extend([empty_lesson] * (min_length - length))

        lesson_list = self.set_breaks_and_period_times(lesson_list, date)

        # Set day_of_week to full regional name
        for lesson in lesson_list:
            lesson.day_of_week = DAY_CHOICES[lesson.day_of_week]
            
        return lesson_list

class UserView(View, DateMixin, CancellationMixin, LessonListMixin):
    """
    Context:
    > announcements = queryset
    > comming_homework = queryset
    > lesson_sets = [lesson_list1, lesson_list2, (...)]
    > legend = queryset

    With:
    lesson_list1 = [<lesson object>, <lesson object>, (...)]
    lesson_list2 = [<lesson object>, <lesson object>, (...)]
    ...

    The day name is done by changing the dayname AFTER the list has been
    created from the queryset
    
    Cancellation is done by creating extra attributes to the lesson objects,
    like is_cancelled and changed_teacher.
    
    The same for period times.
    
    To write:
    class CancellationMixin
        check_cancellation(lesson)
    class LessonListMixin
        shit
    Done | get_lesson_lists()
    Done | get_lesson_set()
    Done | get_date()
    Done | get_allow_weekend()
    Done | check_allow_weekend()
    get_comming_homework()
    get_anouncements()
    get_legend()
    lesson_set_cleanup(*args)
    get_periods_in_day(*args)
    


    PROBLEMS:
    With weekend shit stuff won't work because if check_allow_weekend() returns
    a monday in stead of a saturday, the 2nd day after that wil pass as a monday,
    which will give you 2 mondays O_o -- Solved
    
    Make docstring for sortable_list -- Done
    """
    username_url_kwarg = 'username'
    announcements = None
    comming_homework = None

    def get_announcements(self, date):
        pass

    def get_comming_homework(self, date):
        pass

    def get_legend(self):
        pass

    ## Home Made
    def get_lesson_set(self, date):
        """
        Returns a list of lessons for the given user and date,
        ordered by period
        """

        username = self.kwargs.get(self.username_url_kwarg, None)

        if username is not None:
            try:
                user = User.objects.all().get(username=username)
            except ObjectDoesNotExist:
                raise Http404
        else:
            raise ImproperlyConfigured("UserView needs to be called with "
                                       "a username")

        date = self.check_allow_weekend(date)
        day_of_week = date.strftime('%a')
        lesson_set = user.takes_courses.filter(
            lesson__day_of_week=day_of_week,
            lesson__start_date__lt=date,
            lesson__end_date__gt=date,
        )

        return lesson_set



    # -- Done --
    ## Original
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

    ## Original
    template_name = None
    response_class = TemplateResponse
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )

    ## Edited
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    ## Edited
    def get_context_data(self):
        """
        Get the context for this view.
        """
        date = self.get_date()
        announcements = self.get_announcements(date)
        comming_homework = self.get_comming_homework(date)
        lesson_lists = self.get_lesson_lists(date)
        cancelled_lessons = self.get_cancelled_lessons(lesson_lists, date)
        legend = self.get_legend()

        context = {
            'announcements': announcements,
            'comming_homework': comming_homework,
            'lesson_lists': lesson_lists,
            'legend': legend
        }
        return context