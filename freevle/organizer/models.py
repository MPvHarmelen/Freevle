import datetime
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from freevle.custom.validators import validate_hex


# Create your models here.
# Refactored with some (actually, lots of) help from sushibowl. Thanks :D

# The numbers are chosen to match datetime.date.strftime(<date>,'%w')
DAY_CHOICES = (
    (0, _('Sunday')),
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday')),
)

DAY_DICT = {
    0 : 'Sunday',
    1 : 'Monday',
    2 : 'Tuesday',
    3 : 'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday',
}

class PeriodMeta(models.Model):
    """Defines the length of periods and more"""

    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.IntegerField(choices=DAY_CHOICES)

    period_length = models.IntegerField()
    breaks_after_period = models.CommaSeparatedIntegerField(max_length=32)
    break_lengths = models.CommaSeparatedIntegerField(max_length=32)
    start_of_day = models.TimeField()
    min_periods = models.IntegerField()

    def __unicode__(self):
        return '{} ({} - {})'.format(DAY_DICT[self.day_of_week], self.start_date,
                                     self.end_date)

    def get_period_times(self, periods):
        """
        Get a tuple of starting and ending times of periods
        """
        if periods < self.min_periods:
            periods = self.min_periods
        self.breaks_after_period = [int(i) for i in self.breaks_after_period.split(',')]
        self.break_lengths = [int(i) for i in self.break_lengths.split(',')]
        # make dict of break lengths
        breaks = dict([(value, datetime.timedelta(minutes=self.break_lengths[index])) for
                       index, value in enumerate(self.breaks_after_period)])

        period_times = []
        # We need to use datetime objects instead of time objects, because
        # Python failed on me and can't add timedelta's to time objects.
        # We'll just take the start date to use as a date, but it won't and
        # shouldn't be used anywhere else.
        default_date = {
            'year':self.start_date.year,
            'month':self.start_date.month,
            'day':self.start_date.day,
        }
        start_time = datetime.datetime(
            hour=self.start_of_day.hour,
            minute=self.start_of_day.minute,
            **default_date
        )
        period_length = datetime.timedelta(minutes=self.period_length)
        # Don't forget periods aren't zero based!
        for prev_period in range(periods):
            # If there was a break after the previous period, we need to
            # compensate for that.
            if prev_period in breaks.keys():
                start_time = start_time + breaks[prev_period]

            end_time = start_time + period_length

            # Version 0.bla, Cygnus has a five minute day opening
            if prev_period == 0:
                end_time += datetime.timedelta(minutes=5)

            period_times.append((start_time,end_time))
            start_time = end_time

        period_times = tuple(period_times)
        return period_times

def get_periodmeta(date):
    """
    Rules:
        1. smallest (end_date - start_date) wins
        2. shortest period wins
        3. least number of breaks wins
        4. Error, the one who filled out the times sucks
    """
    queryset = PeriodMeta.objects.filter(
        start_date__lt = date,
        end_date__gt = date,
        day_of_week = int(date.strftime('%w'))
    )

    if len(queryset) == 0:
        raise ImproperlyConfigured('There is no periodmeta set for {}'
                                 ''.format(date))

    if len(queryset) == 1:
        periodmeta = queryset[0]
    else:
        # Check rule 1
        date_len = lambda a: a.end_date - a.start_date
        smallest_date_len = min([date_len(a) for a in queryset])
        periodmeta_set = [a for a in queryset
                             if date_len(a) == smallest_date_len]

        if len(periodmeta_set) == 1:
            periodmeta = periodmeta_set[0]
        else:
            # Check rule 2
            shortest_period = min([a.period for a in periodmeta_set])
            periodmeta_set = ([a for a in periodmeta_set
                                 if a.period == shortest_period])

            if len(periodmeta_set) == 0:
                periodmeta = periodmeta_set[0]
            else:
                # Check rule 3
                least_breaks = min([len(a.breaks_after_period) for a in
                                    periodmeta_set])
                periodmeta_set = min(
                   [a for a in periodmeta_set
                    if len(a.breaks_after_period) == least_breaks]
                )

                if len(periodmeta_set) == 0:
                    periodmeta = periodmeta_set[0]
                    periodmeta = periodmeta_set[0]
                else:
                    # Rule 4
                    raise ImproperlyConfigured(
                        'There are too many PeriodMetas defined. '
                        'Please contact your administrators and tell them '
                        "they're idiots and can't even configure "
                        'PeriodMetas. Thank you.'
                    )

    return periodmeta

class Topic(models.Model):
    name = models.CharField(max_length=32, unique=True)
    abbr = models.CharField(max_length=4, unique=True)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(unique=True)
    topic = models.ForeignKey(Topic)
    teacher = models.ForeignKey(
        User,
        related_name='gives_courses',
        limit_choices_to={'groups__name': 'teachers'}
    )
    students = models.ManyToManyField(
        User,
        related_name='takes_courses',
        limit_choices_to={'groups__name': 'students'}
    )

    class Meta:
        unique_together = ('name', 'teacher')

    def __unicode__(self):
        return '{} ({})'.format(self.topic, self.teacher.get_profile().designation)

class Classroom(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course)
    classroom = models.ForeignKey(Classroom)

    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    period = models.IntegerField()

    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return '{} {} {}'.format(self.course.topic, DAY_DICT[self.day_of_week],
                                 self.period)

class HomeworkType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    abbr = models.CharField(max_length=8)
    color = models.CharField(max_length=7, validators=[validate_hex])
    weight = models.IntegerField(help_text=_('Homework with a weight higher '
                                              'than 10 will appear under '
                                              '`comming homework`'))

    def __cmp__(self, other):
        return cmp(self.weight, other.weight)

    def __eq__(self, other):
        return super(HomeworkType).__eq__(self, other)

    def __unicode__(self):
        return self.name

class Homework(models.Model):
    homework_type = models.ForeignKey(HomeworkType)
    content = models.CharField(max_length=255)

    course = models.ForeignKey(Course)
    due_date = models.DateField()
    period = models.IntegerField(null=True, blank=True)

    def __eq__(self, other):
        if type(self) == type(other):
            def extended_and(li):
                if len(li) > 1:
                    return li.pop() and extended_and(li)
                else:
                    return li[0]
            attrs = ['homework_type', 'content', 'course', 'due_date', 'period']
            return extended_and(getattr(self, attr) == getattr(other, attr) for
                                attr in attrs)
        else:
            return False

    def __unicode__(self):
        return '{} {} on {}'.format(self.course.topic, self.homework_type,
                                    self.due_date.strftime('%d-%m-%Y'))

    class Meta:
        verbose_name_plural = 'homework'

class ChangedLesson(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        related_name='changed'
    )
    date = models.DateField()
    new_date = models.DateField(
        blank=True,
        null=True
    )
    new_teacher = models.ForeignKey(
        User,
        blank=True,
        null=True,
        limit_choices_to={'groups__name':'teachers'}
    )
    new_classroom = models.ForeignKey(
        Classroom,
        blank=True,
        null=True
    )
    new_period = models.IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('lesson', 'date')

    def __unicode__(self):
        return 'Modification of {} on {}'.format(self.lesson,
                                                 self.date.strftime('%d-%m-%Y'))


class CancelledTeacher(models.Model):
    teacher = models.ForeignKey(
        User,
        limit_choices_to={'groups__name':'teachers'},
        related_name='cancelled'
    )
    start_date = models.DateField()
    start_period = models.IntegerField()
    end_date = models.DateField()
    end_period = models.IntegerField()

    def __unicode__(self):
        return 'Modification of {} from {} to {}'.format(self.teacher,
                                                 self.start_date.strftime('%d-%m-%Y'),
                                                 self.end_date.strftime('%d-%m-%Y'))

class CancelledClassroom(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        related_name='cancelled'
    )
    start_date = models.DateField()
    start_period = models.IntegerField()
    end_date = models.DateField()
    end_period = models.IntegerField()

    def __unicode__(self):
        return 'Modification of {} from {} to {}'.format(self.classroom,
                                                 self.start_date.strftime('%d-%m-%Y'),
                                                 self.end_date.strftime('%d-%m-%Y'))

class Announcement(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return content
