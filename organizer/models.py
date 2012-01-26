from django.db import models
from cygy.custom import fields
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Lesson(models.Model):
	teacher = models.ForeignKey(User,
			limit_choices_to={'groups_in': ['teachers']})
	topic = models.ForeignKey(Topic)
	pupils = models.ManyToMany(User,
			limit_choices_to={'groups_in':['pupils']})
	time = models.ManyToMany(Time)

#class Time(models.Model):
#	DAY_CHOICES = (
#		('MON', _('Monday'))
#		('TUE', _('Tuesday'))
#		('WEN', _('Wednesday'))
#		('THU', _('Thursday'))
#		('FRI', _('Friday'))
#	)
#	day = models.CharField(max_length=3, choices=DAY_CHOICES)
#	period = models.IntegerField()

class Homework(models.Model):
	type = models.ForeignKey(HomeworkType)
	content = models.CharField(max_length=255)
	lesson = models.ForeignKey(Lesson)
	time = models.ForeignKey
	 
	
