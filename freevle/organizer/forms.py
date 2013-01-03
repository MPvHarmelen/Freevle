from django.forms import ModelForm
from django.forms.formsets import formset_factory

from freevle.organizer.models import Homework

class HomeworkForm(ModelForm):
    class Meta:
        model = Homework
        fields = ('homework_type', 'content',)
