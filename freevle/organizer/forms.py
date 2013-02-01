from django import forms
from django.forms.formsets import formset_factory

from freevle.organizer.models import Homework, Course

class HCourseForm(forms.Form):
    def __init__(self, **kwargs):
        courses = kwargs.pop('courses')
        return super(HCourseForm, self).__init__(**kwargs)
        self.fields['course'].queryset = courses

    course = forms.ModelChoiceField(queryset=Course.objects.none())



class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('homework_type', 'content',)
