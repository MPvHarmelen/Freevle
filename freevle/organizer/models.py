import datetime
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from freevle.custom.validators import validate_hex


# Create your models here.
# Refactored with some (actually, lots of) help from sushibowl. Thanks :D

# The case for the abbreviations are chosen
# to match the %a format of strftime(), the order to match %w.
DAY_CHOICES = (
    ('Sun', _('Sunday')),
    ('Mon', _('Monday')),
    ('Tue', _('Tuesday')),
    ('Wed', _('Wednesday')),
    ('Thu', _('Thursday')),
    ('Fri', _('Friday')),
    ('Sat', _('Saturday')),
)

class PeriodMeta(models.Model):
    """Defines the length of periods and more"""

    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)

    period_length = models.IntegerField()
    breaks_after_period = models.CommaSeparatedIntegerField(max_length=32)
    break_lengths = models.CommaSeparatedIntegerField(max_length=32)
    start_of_day = models.TimeField()
    min_periods = models.IntegerField()

    def __unicode__(self):
        return '{} ({} - {})'.format(self.day_of_week, self.start_date,
                                     self.end_date)

    def get_periodmeta(self, date):
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
            day_of_week = date.strftime('%a')
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
                    else:
                        # Rule 4
                        raise ImproperlyConfigured(
                            'There are too many Periodlengths defined. '
                            'Please contact your administrators and tell them '
                            "they're idiots and can't even configure "
                            'Periodlengths. Thank you.'
                        )

        return periodmeta

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

class Topic(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class Course(models.Model):
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

    def __unicode__(self):
        return '{} ({})'.format(self.topic, self.teacher.get_profile().designation)

class Classroom(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course)
    classroom = models.ForeignKey(Classroom)

    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    period = models.IntegerField()

    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return '{} {} {}'.format(self.course.topic, self.day_of_week,
                                 self.period)

class HomeworkType(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=8)
    color = models.CharField(max_length=7, validators=[validate_hex])
    weight = models.IntegerField(help_text=_('Homework with a weight higher '
                                              'than 10 will appear under '
                                              '`comming homework`'))

    def __unicode__(self):
        return self.name

class Homework(models.Model):
    homework_type = models.ForeignKey(HomeworkType)
    content = models.CharField(max_length=255)

    lesson = models.ForeignKey(Lesson)
    due_date = models.DateField()

    def __unicode__(self):
        return '{} {}'.format(self.homework_type, self.lesson.course.topic)

    class Meta:
        verbose_name_plural = 'homework'

class Cancellation(models.Model):
    teacher = models.ForeignKey(
        User,
        related_name='cancelled_teacher',
        blank=True, null=True,
        limit_choices_to={'groups__name': 'teachers'}
    )
    new_teacher = models.ForeignKey(
        User,
        related_name='replacement_teacher',
        blank=True, null=True,
        limit_choices_to={'groups__name': 'teachers'}
    )

    classroom = models.ForeignKey(
        Classroom,
        blank=True,
        null=True,
        related_name='cancelled_classroom'
    )
    new_classroom = models.ForeignKey(
        Classroom,
        blank=True,
        null=True,
        related_name='replacement_classroom'
    )

    date = models.DateTimeField()
    begin_period = models.IntegerField()
    end_period = models.IntegerField()

    def __unicode__(self):
        return '{} from {} to {}'.format(self.date, self.begin_period, self.end_period)

class Announcements(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return content
