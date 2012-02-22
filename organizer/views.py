# Create your views here.

import datetime

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from cygy.organizer.models import Lesson

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

    ## Edited
    def get_month(self):
        """
        Return the day for which this view should display data
        """
        month = self.month
        if month is None:
            try:
                month = self.kwargs['month']
            except KeyError:
                month = datetime.date.today().month

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
        allow_weekend = self.get_allow_weekend

        if not allow_weekend:
            if date.strftime('%a') is 'Sat':
                date += datetime.timedelta(days=2)
            elif date.strftime('%a') is 'Sat':
                date += datetime.timedelta(days=1)

        return date



    ## Brewed from _date_from_string(kwargs)
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
    # You have to be careful with this empty_lesson, because empty
    # ForeignKey fields raise DoesNotExist. Also the __unicode__ raises
    # DoesNotExist (because it uses the value of a ForeignKey,
    # so don't try using empty_lesson in command line!
    empty_lesson = Lesson()
        

    def get_lesson_set(self, obj, date):
        '''
        Returns an iterable of lessons for the given date and object.
        '''
        raise ImproperlyConfigured('You must write your own get_lesson_list')
        

    # Homemade
    lesson_lists = None
    def get_lesson_lists(self, date):
        """
        Get the list of lessonsets. This is a list of querysets.
        """
        if self.lesson_lists is not None:
            lesson_lists = self.lesson_lists
        else:
            obj = self.get_obj()

            number_days = self.get_number_days()
            lesson_lists = [self.get_lesson_list(user,
                                                 date + datetime.timedelta(days=n))
                            for n in range(number_days)]
        
            
        for lesson_list in lesson_lists:
            #lesson_list += [''] * (N-len(lesson))
            lesson_list = lesson_set_cleanup(lesson_set,date,length)
        
        return lesson_lists
        
    def lesson_set_cleanup(self, lesson_set, date):
        """
        Takes an iterable of lessons, returns a lesson_list checked for
        cancellation of at least PERIODS_IN_DAY lessons long and with
        lesson.day_of_week set to full regional name.
        """
        empty_lesson = self.empty_lesson
        
        # list() is needed because querysets don't support backwards indexing
        unpadded_list = list(lesson_set)
        unpadded_list.sort(key=lambda a: a.period)

        lesson_list = []
        for i in range(len(unpadded_list)):
            if i == 0:
                previous_period = 0
            else:
                previous_period = unpadded_list[i - 1].period

            if lesson_set[i].period != previous_period + 1:
                difference = lesson_set[i] - previous_period
                # Two adjacent hours differ 1
                lesson_list.extend([empty_lesson] * (difference - 1))
            else:
                lesson_list.append(lesson_set[i])

        lesson_list = self.check_cancellation(lesson_list)
        
        # Some last perfections
        len_diff = len(lesson_set) - self.get_periods_in_day()
        if len_diff > 0:
            lesson_list.extend([empty_lesson for i in range(len_diff)])

        for lesson in lesson_list:
            day_of_week = date.strftime('%A')
            lesson.day_of_week = _(day_of_week)
            
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

    The day name is done by updating the queryset of a day to make
    day_of_week a full name, instead of an English abbreviation
        !! We are not going to use update, because it changes the database !!

    So, the day name is done by changing the dayname AFTER the list has been
    created from the queryset
    
    Cancellation is done by creating extra attributes to the lesson objects,
    like is_cancelled and changed_teacher.
    
    To write:
    class CancellationMixin
    get_comming_homework()
    get_anouncements()
    Done | get_lesson_lists()
    get_lesson_list()
    Done | get_date()
    get_legend()
    Done | get_allow_weekend()
    Done | check_allow_weekend()
    get_PERIODS_IN_DAY()

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

    def get_obj(self):
                                                                    # << HERE!!!
        username = self.kwargs.get(self.username_url_kwarg, None)

        if username is not None:
            try:
                user = User.objects.all().get(username=username)
            except ObjectDoesNotExist:
                raise Http404
        else:
            raise ImproperlyConfigured("UserView needs to be called with "
                                       "a username")


    ## Home Made
    def get_lesson_list(self, user, date):
        """
        Returns a list of lessons for the given user and date,
        ordered by period
        """
        date = self.check_allow_weekend(date)
        day_of_week = date.strftime('%a')
        lesson_set = user.takes_courses.filter(
            lesson__day_of_week=day_of_week
            lesson__start_date__lt=date
            lesson__end_date__gt=date
        )

        return lesson_list    



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




# I'm just leaving this here for now if I want to use parts later
def _get_next_prev_month(generic_view, naive_result, is_previous, use_day_names):
    """
    Helper: Get the next or the previous valid date. The idea is to allow
    links on month/day views to never be 404s by never providing a date
    that'll be invalid for the given view.

    This is a bit complicated since it handles both next and previous months
    and days (for MonthArchiveView and DayArchiveView); hence the coupling to generic_view.

    However in essence the logic comes down to:

        * If allow_empty and allow_future are both true, this is easy: just
          return the naive result (just the next/previous day or month,
          reguardless of object existence.)

        * If allow_empty is true, allow_future is false, and the naive month
          isn't in the future, then return it; otherwise return None.

        * If allow_empty is false and allow_future is true, return the next
          date *that contains a valid object*, even if it's in the future. If
          there are no next objects, return None.

        * If allow_empty is false and allow_future is false, return the next
          date that contains a valid object. If that date is in the future, or
          if there are no next objects, return None.

    """
    date_field = generic_view.get_date_field()
    allow_empty = generic_view.get_allow_empty()
    allow_future = generic_view.get_allow_future()

    # If allow_empty is True the naive value will be valid
    if allow_empty:
        result = naive_result

    # Otherwise, we'll need to go to the database to look for an object
    # whose date_field is at least (greater than/less than) the given
    # naive result
    else:
        # Construct a lookup and an ordering depending on whether we're doing
        # a previous date or a next date lookup.
        if is_previous:
            lookup = {'%s__lte' % date_field: naive_result}
            ordering = '-%s' % date_field
        else:
            lookup = {'%s__gte' % date_field: naive_result}
            ordering = date_field

        qs = generic_view.get_queryset().filter(**lookup).order_by(ordering)

        # Snag the first object from the queryset; if it doesn't exist that
        # means there's no next/previous link available.
        try:
            result = getattr(qs[0], date_field)
        except IndexError:
            result = None

    # Convert datetimes to a dates
    if hasattr(result, 'date'):
        result = result.date()

    # For month views, we always want to have a date that's the first of the
    # month for consistency's sake.
    if result and use_day_names:
        result = result.replace(day=1)

    # Check against future dates.
    if result and (allow_future or result < datetime.date.today()):
        return result
    else:
        return None






class UserDetailView(DetailView):
    username_field = 'username'
    username_url_kwarg = 'username'

    def get_object(self, queryset=None):


        # Use a custom queryset if provided
        if queryset is None:
            queryset = self.get_queryset()

        username = self.kwargs.get(self.username_url_kwarg, None)

        # Try looking up by username.
        if username is not None:
            username_field = self.username_field
            queryset = queryset.filter(**{username_field: username})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u'Generic detail view {} must be called with '
                                 u'a username.'.format(self.__class__.__name__))

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(
                _(u'No {verbose_name} found matching the query').format(
                    verbose_name=queryset.model._meta.verbose_name
                    )
                )
        return obj
