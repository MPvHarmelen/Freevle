import datetime
import warnings
import copy

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from freevle.organizer.models import *

# You have to be careful with EmptyLesson, because empty
# ForeignKey fields raise DoesNotExist.

class StrCourse(Course):
    """
    This is a derivative  of freevle.organizer.Course, but with the foreignkey
    for the topic changed into a string. Like this it can be used for an
    empty lesson, without raising errors or having to change a lot of
    complicated code.
    """
    topic = str()

class DateMixin(object):
    year = None
    month = None
    day = None

    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'

    allow_weekend = False
    number_days = 5

    def get_number_days(self):
        return self.number_days

    def get_year(self):
        """
        Return the (still formatted) year for which this view should display data
        """
        year = self.year
        if year is None:
            try:
                year = self.kwargs['year']
            except KeyError:
                year = datetime.date.today().year
        return str(year)

    def get_month(self):
        """
        Return the (still formatted) month for which this view should display data
        """
        month = self.month
        if month is None:
            try:
                month = self.kwargs['month']
            except KeyError:
                month = datetime.date.today().month
        return str(month)

    def get_day(self):
        """
        Return the (still formatted) day for which this view should display data
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

class ModificationMixin(object):
    warnings.warn("\n\n\t ModificationMixin isn't working correctly!\n")

    def cancelled_classroom(self, classroom, period, date):
        '''Checks if a classroom is cancelled.'''
        part1 = list(classroom.cancelled.filter(
            start_date=date,
            start_period__lte=period
        ))
        part2 = list(classroom.cancelled.filter(
            start_date__lt=date,
            end_date__gt=date
        ))
        part3 = list(classroom.cancelled.filter(
            end_date=date,
            end_period__lte=period
        ))
        changes = part1 + part2 + part3

        if len(changes) > 0:
            return True
        else:
            return False

    def cancelled_teacher(self, teacher, period, date):
        '''Checks if a teacher is cancelled.'''
        part1 = list(teacher.cancelled.filter(
            start_date=date,
            start_period__lte=period
        ))
        part2 = list(teacher.cancelled.filter(
            start_date__lt=date,
            end_date__gt=date
        ))
        part3 = list(teacher.cancelled.filter(
            end_date=date,
            end_period__lte=period
        ))
        changes = part1 + part2 + part3

        if len(changes) > 0:
            return True
        else:
            return False

    def modify_lesson(self, lesson, date):
        '''
        Modifies a lesson according to cancelled classroom, teacher or `changed`
        attribute.
        '''
        lesson = copy.copy(lesson)
        lesson.classroom = copy.copy(lesson.classroom)
        if self.cancelled_classroom(lesson.classroom, lesson.period, date):
            lesson.classroom.is_cancelled = True
        else:
            lesson.classroom.is_cancelled = False
        lesson.course = copy.copy(lesson.course)
        lesson.course.teacher = copy.copy(lesson.course.teacher)
        if self.cancelled_teacher(lesson.course.teacher, lesson.period, date):
            lesson.course.teacher.is_cancelled = True
        else:
            lesson.course.teacher.is_cancelled = False

        try:
            changes = lesson.changed.get(date=date)
            if changes.new_teacher is not None:
                lesson.course = copy.copy(lesson.course)
                lesson.course.teacher = copy.copy(changes.new_teacher)
                lesson.course.teacher.is_changed = True
                lesson.course.teacher.is_cancelled = False
            if changes.new_classroom is not None:
                lesson.classroom = copy.copy(changes.new_classroom)
                lesson.classroom.is_changed = True
                lesson.classroom.is_cancelled = False
            lesson.period = changes.new_period or lesson.period
        except ChangedLesson.DoesNotExist:
            pass

        lesson.is_cancelled = lesson.course.teacher.is_cancelled or lesson.classroom.is_cancelled

        return lesson


class HomeworkMixin(object):
    coming_homework_days = 14
    coming_homework_min_weight = 10
    coming_homework = None

    def set_homework(self, lesson, date):
        key = lambda a: a.homework_type.weight
        lesson.homework = sorted(
            [homework for homework in lesson.homework_set.filter(
                due_date=date
             )],
            key=key,
            # A higher weight is more important & more important homework
            # should go first, thus:
            reverse=True
        )
        return lesson

    def get_coming_homework(self, date, user):
        coming_homework = self.coming_homework

        if coming_homework is None:
            min_weight = self.coming_homework_min_weight
            days = self.coming_homework_days
            end_date = date + datetime.timedelta(days=days)
            coming_homework = []

            for course in user.takes_courses.all():
                for lesson in course.lesson_set.all():
                    coming_homework.extend(
                        lesson.homework_set.filter(
                            due_date__gte=date,
                            due_date__lte=end_date,
                            homework_type__weight__gte=min_weight
                        )
                    )

        return coming_homework

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
        latest_period = len(lesson_list)
        period_times = periodmeta.get_period_times(latest_period)

        for index, time in enumerate(period_times):
            lesson_list[index].start_time = time[0].strftime('%H:%M')
            lesson_list[index].end_time = time[1].strftime('%H:%M')

        return lesson_list

    def get_lesson_set(self, date):
        '''
        Returns an iterable of lessons for the given date and object.
        '''
        raise ImproperlyConfigured('You must write your own `get_lesson_set`.')

    def get_obj(self):
        '''
        Returns the object for which this view is generating an organizer.
        '''
        raise ImproperlyConfigured('You must write your own `get_obj`.')

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
            length = self.get_min_periods(date)
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
                # Add the day of week for the template.
                lesson_set.insert(0, _(date.strftime('%A')))
                lesson_lists[index] = lesson_set

        return lesson_lists

    def lesson_set_cleanup(self, lesson_set, min_length, date):
        """
        Takes an iterable of lessons, returns a lesson_list ready to be
        iterated for the template. (No cancellation is checked)
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
            lesson_list.extend(empty_lesson() for i in range(min_length - length))

        lesson_list = self.set_period_times(lesson_list, date)

        return lesson_list

class OrganizerView(TemplateView, LessonListMixin):
    announcements = None

    def get_announcements(self, date):
        announcements = self.announcements
        if announcements is None:
            announcements = Announcement.objects.filter(
                start_date__lte=date,
                end_date__gte=date
            )

        return announcements

    def get_coming_homework(self, date, obj):
        return None

    def get_legend(self):
        return HomeworkType.objects.all()

    def get_period_range(self, lesson_lists):
        return range(1, len(lesson_lists[0]))

    def get_context_data(self, **kwargs):
        """ Get the context for this view. """
        date = self.get_date()
        obj = self.get_obj()
        announcements = self.get_announcements(date)
        lesson_lists = self.get_lesson_lists(date, obj)
        legend = self.get_legend()
        period_range = self.get_period_range(lesson_lists)

        context = {
            'announcements': announcements,
            'lesson_lists': lesson_lists,
            'legend': legend,
            'period_range': period_range,
        }

        try:
            get_coming_homework = self.get_coming_homework
        except AttributeError:
            def get_coming_homework(date, obj):
                pass

        coming_homework = self.get_coming_homework(date, obj)

        if coming_homework is not None:
            context['coming_homework'] = coming_homework

        context.update(kwargs)
        return context

class StudentPrintView(OrganizerView):
    template_name = 'organizer/student_organizer.html'
    username_url_kwarg = 'username'
    user = None

    def get_obj(self):

        if self.user is not None:
            return self.user
        elif username is not None:
            username = self.kwargs.get(self.username_url_kwarg, None)
            try:
                user = User.objects.get(username=username,
                                        groups__name='students')
            except User.DoesNotExist:
                raise Http404("There is no student with this username.")
        else:
            raise ImproperlyConfigured("StudentView should be called with "
                                       "a user or username")
        return user

    ## Home Made
    def get_lesson_set(self, date, user):
        """
        Returns a list of lessons for the given user and date.
        """

        day_of_week = date.strftime('%a')
        lesson_list = []
        for course in user.takes_courses.all():
            lesson_subset = course.lesson_set.filter(
                day_of_week=day_of_week,
                start_date__lte=date,
                end_date__gte=date
            )
            lesson_list.extend(lesson_subset)
        return lesson_list

class StudentView(StudentPrintView, ModificationMixin, HomeworkMixin):
    def get_lesson_set(self, date, user):
        """
        Returns a list of lessons for the given user and date with homework
        and modifications.
        """
        day_of_week = date.strftime('%a')
        lesson_list = []
        for course in user.takes_courses.all():
            lesson_subset = course.lesson_set.filter(
                day_of_week=day_of_week,
                start_date__lte=date,
                end_date__gte=date
            )
            for lesson in lesson_subset:
                lesson = self.set_homework(lesson, date)
                lesson = self.modify_lesson(lesson, date)
                lesson_list.append(lesson)
        return lesson_list



class TeacherPrintView(OrganizerView):
    template_name = 'organizer/teacher_organizer.html'
    username = None
    user = None

    def get_obj(self):

        if self.user is not None:
            return self.user
        elif self.username is not None:
            try:
                user = User.objects.get(username=username,
                                        groups__name='teachers')
            except User.DoesNotExist:
                raise Http404("There is no teacher with this username.")
        else:
            raise ImproperlyConfigured("TeacherView should be called with "
                                       "a user or username")
        return user

    def get_lesson_set(self, date, user):
        """
        Returns a list of lessons for the given user and date.
        """
        day_of_week = date.strftime('%a')
        lesson_list = []
        for course in teacher.gives_courses.all():
            lesson_subset = course.lesson_set.filter(
                day_of_week=day_of_week,
                start_date__lte=date,
                end_date__gte=date
            )
            lesson_list.extend(lesson_subset)
        return lesson_list

class TeacherView(TeacherPrintView, ModificationMixin):
    def get_lesson_set(self, date, teacher):
        day_of_week = date.strftime('%a')
        lesson_list = []
        for course in teacher.gives_courses.all():
            lesson_subset = course.lesson_set.filter(
                day_of_week=day_of_week,
                start_date__lte=date,
                end_date__gte=date
            )
            lesson_list.extend(lesson_subset)

        for changes in ChangedLesson.objects.filter(new_teacher=teacher,
                                                    date=date):
            lesson = copy.copy(changes.lesson)
            lesson.is_changed = True
            lesson_list.append(lesson)

        lesson_list2 = []
        for lesson in lesson_list:
            lesson_list2.append(self.modify_lesson(lesson, date))

        return lesson_list2

class ClassroomPrintView(OrganizerView):
    template_name = 'organizer/classroom_organizer.html'
    classroom_url_kwarg = 'classroom'
    classroom = None

    def get_obj(self):
        name = self.kwargs.get(self.classroom_url_kwarg, None)

        if self.classroom is not None:
            classroom = self.classroom
        elif name is not None:
            try:
                classroom = Classroom.objects.get(name=name)
            except Classroom.DoesNotExist:
                raise Http404("There is no classroom with this name.")
        else:
            raise ImproperlyConfigured("ClassroomView should be called with "
                                       "a classroom or name.")
        return classroom

    ## Home Made
    def get_lesson_set(self, date, classroom):
        """
        Returns a list of lessons for the given classroom and date.
        """

        day_of_week = date.strftime('%a')
        lesson_list = list(classroom.lesson_set.filter(
            start_date__lte=date,
            end_date__gte=date,
            day_of_week=day_of_week
        ))
        return lesson_list

class ClassroomView(ClassroomPrintView, ModificationMixin):
    def get_lesson_set(self, date, classroom):
        day_of_week = date.strftime('%a')
        lesson_list = list(classroom.lesson_set.filter(
            start_date__lte=date,
            end_date__gte=date,
            day_of_week=day_of_week
        ))

        for changed in ChangedLesson.objects.filter(new_classroom=classroom,
                                                    date=date):
            lesson = copy.copy(changed.lesson)
            lesson.is_changed = True
            lesson_list.append(lesson)

        lesson_list2 = []
        for lesson in lesson_list:
            lesson_list2.append(self.modify_lesson(lesson))

        return lesson_list2


def organizer_view(request, **kwargs):
    slug = kwargs.pop('slug', None)
    if slug is not None:
        try:
            # __iexact makes for a case insensitive lookup
            user = User.objects.get(username__iexact=slug)
            group_names = [group.name for group in user.groups.all()]
            if 'students' in group_names:
                return StudentView.as_view(user=user, **kwargs)(request)
            elif 'teachers' in group_names:
                return TeacherView.as_view(user=user, **kwargs)(request)
            else:
                raise Http404("This user isn't a student or a teacher.")
        except User.DoesNotExist:
            try:
                classroom = Classroom.objects.get(name__iexact=slug)
                return ClassroomView.as_view(classroom=classroom, **kwargs)(request)
            except Classroom.DoesNotExist:
                raise Http404("This slug isn't a username or classroom.")
    else:
        raise ImproperlyConfigured("organizer_view mast be called with a slug.")
