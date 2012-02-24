from django.db import models
from cygy.custom import fields
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

    length = models.IntegerField()
    brakes_after_period = models.CommaSeparatedIntegerField(max_length=32)
    start_of_day = models.TimeField()
    min_periods = models.IntegerField()

    def get_periodlength_object(self, date):
        queryset = self.objects.filter(
            start_date__lt = date,
            start_date__gt = date,
            day_of_week = date.strftime('%a'),
        )
        
        if len(queryset) == 1:
            object = queryset[0]
        else:
            #key = lambda a: a.                                 ## << Here
        
    
    def is_next_period_break(self, date, period):
        periodlength_object = self.get_periodlength_object(date)
        
        if period in periodlength_object.brakes_after_period:
            return True
        else:
            return False

    def get_period_times(self, date, periods):
        """Get a list of starting and ending times of periods

        Please note that the argument date's supposed to be a datetime.date
        object.
        
        way to return:
        if periods < self.min_periods:
            periods = self.min_periods
        period_times = list()
        for i in range(periods)
            calculate shit
            period_times.append((sart_time,end_time,is_break))
        
        period_times = tuple(period_times)
        return period_times
         
        """
        
        if periods < self.min_periods:
            periods = self.min_periods

        period_times = []
        for i in range(periods):
            # calculate shit
            periodlength_object = self.get_periodlength_object(date)
            period_times.append((sart_time,end_time,is_break))
        
        period_times = tuple(period_times)
        return period_times

        pass

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
