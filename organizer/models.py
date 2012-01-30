from django.db import models
from cygy.custom import fields
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=8)

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
    teacher = models.ForeignKey(User,
            limit_choices_to={'groups_in': ['teachers']})
    topic = models.ForeignKey(Topic)
    classroom = models.CharField(max_length=16)
    period = models.IntegerField()
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)

class TimeTable(models.Model):
    date_of_monday = models.DateField()
    lessons = models.ManyToManyField(Lesson)
    user = models.ForeignKey(User) 

class HomeworkType(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=8)
    color = fields.HexColorField()

class Homework(models.Model):
    type = models.ForeignKey(HomeworkType)
    content = models.CharField(max_length=255)
    timetable = models.ForeignKey(TimeTable) 
    lesson = models.ForeignKey(Lesson)
