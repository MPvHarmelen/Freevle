from django.db import models
from cygy.custom import fields
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
# Refactored with some (actually, lots of) help from sushibowl. Thanks :D
class Topic(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=16)
        
    def __unicode__(self):
        return name

class Course(models.Model):
    topic = models.ForeignKey(Topic)
    teacher = models.ForeignKey(
        User,
        related_name='course_given',
        limit_choices_to={'groups__name': 'teachers'}
    )
    students = models.ManyToManyField(
        User,
        related_name='course_taken',
        limit_choices_to={'groups__name': 'students'}
    )
    
    def __uncidode(self):
        return '{} ({})'.format(topic.__unicode__(), teacher.designation)

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

class HomeworkType(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=8)
    color = fields.HexColorField()

class Homework(models.Model):
    type = models.ForeignKey(HomeworkType)
    content = models.CharField(max_length=255)

    lesson = models.ForeignKey(Lesson)
    due_date = models.DateField()

class Cancellation(models.Model):
    teacher = models.ForeignKey(User, blank=True, null=True,
            limit_choices_to={'groups__name': 'teachers'})
    classroom = models.CharField(max_length=16, blank=True)
    date = models.DateTimeField()
    time = models.DateTimeField()
