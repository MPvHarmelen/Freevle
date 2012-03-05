import datetime
from django.db import models
from cygy.custom import fields
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
# Refactored with some (actually, lots of) help from sushibowl. Thanks :D

# The case for the abbreviations are chosen
# to match the %a format of strftime(), the order to match %w.
DAY_CHOICES = (
    ('Sun', _('Sunday')),
    ('Mon', _('Monday')),
    ('Tue', _('Tuesday')),
    ('Wen', _('Wednesday')),
    ('Thu', _('Thursday')),
    ('Fri', _('Friday')),
    ('Sat', _('Saturday')),
)

class PeriodLengths(models.Model):
    """Defines the length of periods and more"""
    
    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)

    period_length = models.IntegerField()
    breaks_after_period = models.CommaSeparatedIntegerField(max_length=32)
    break_lengths = models.CommaSeparatedIntegerField(max_length=32)
    start_of_day = models.TimeField()
    min_periods = models.IntegerField()

    def get_periodlengths(self, date):
        """
        Rules:
            1. smallest (end_date - start_date) wins
            2. shortest period wins
            3. least number of breaks wins
            4. Error, the one who filled out the times sucks
        """
        queryset = PeriodLengths.objects.filter(
            start_date__lt = date,
            end_date__gt = date,
            day_of_week = date.strftime('%a'),
        )

        if len(queryset) == 0:
            raise ObjectDoesNotExist

        if len(queryset) == 1:
            periodlengths = queryset[0]
        else:
            # Check rule 1
            date_len = lambda a: a.end_date - a.start_date
            smallest_date_len = min([date_len(a) for a in queryset])
            periodlengths_set = [a for a in queryset
                                 if date_len(a) == smalles_date_len]
            
            if len(periodlengths_set) == 1:
                periodlengths = periodlengths_set[0]
            else:
                # Check rule 2
                shortest_period = min([a.period for a in periodlengths_set])
                periodlengths_set = ([a for a in periodlengths_set
                                     if a.period == shortest_period])

                if len(periodlengths_set) == 0:
                    periodlengths = periodlengths_set[0]
                else:
                    # Check rule 3
                    least_breaks = min([len(a.breaks_after_period) for a in
                                        periodlengths_set])
                    periodlengths_set = min(
                       [a for a in periodlengths_set
                        if len(a.breaks_after_period) == least_breaks]
                    )

                    if len(periodlengths_set) == 0:
                        periodlengths = periodlengths_set[0]
                    else:
                        # Rule 4
                        raise ImproperlyConfigured(
                            'There are too many Periodlengths defined. '
                            'Please contact your administrators and tell them '
                            "they're idiots and can't even configure "
                            'Periodlengths. Thank you.'
                        )

        return periodlengths
    
    def is_next_period_break(self, period):
        """Returns if there is a break after this period"""
        if period in self.brakes_after_period:
            return True
        else:
            return False

    def get_period_times(self, periods):
        """
        Get a tuple of starting and ending times of periods and breaks
        """
        if periods < self.min_periods:
            periods = self.min_periods
        
        # make dict of break lengths
        breaks = dict([(value, self.break_lengths[index]) for
                       index, value in enumerate(breaks_after_period)])
        
        period_times = []
        start_time = self.start_of_day
        period_length = self.period_length
        
        for period in range(periods):
            if period in breaks.keys():
                duration = breaks[period]
                is_break = True
            else:
                duration = period_length
                is_break = False
            
            end_time = start_time + duration
            period_times.append((sart_time,end_time,is_break))
        
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

class Lesson(models.Model):
    course = models.ForeignKey(Course)
    classroom = models.CharField(max_length=16)

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
    color = fields.HexColorField()

    def __unicode__(self):
        return self.name

class Homework(models.Model):
    homework_type = models.ForeignKey(HomeworkType)
    content = models.CharField(max_length=255)

    lesson = models.ForeignKey(Lesson)
    due_date = models.DateField()

    def __unicode__(self):
        return '{} {}'.format(self.homework_type, self.lesson.course.topic)

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
    
    classroom = models.CharField(max_length=16, blank=True)
    new_classroom = models.CharField(max_length=16, blank=True)
    
    date = models.DateTimeField()
    begin_period = models.IntegerField()
    end_period = models.IntegerField()

    def __unicode__(self):
        return '{} from {} to {}'.format(self.date, self.begin_period, self.end_period)
