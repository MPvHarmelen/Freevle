from django.db import models
from cygy.custom import fields
from django.core.validators import EMPTY_VALUES
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
# Refactored with some (actually, lots of) help from sushibowl. Thanks :D
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
    DAY_CHOICES = (
        ('MON', _('Monday')),
        ('TUE', _('Tuesday')),
        ('WEN', _('Wednesday')),
        ('THU', _('Thursday')),
        ('FRI', _('Friday')),
        ('SAT', _('Saturday')),
        ('SUN', _('Sunday')),
    )
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
        related_name='new_teacher',
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
