from django import forms
from django.forms.formsets import formset_factory

from freevle.organizer.models import Homework

class HCourseForm(forms.Form):
    def __init__(self, **kwargs):
        self.teacher = kwargs.pop('teacher')
        return super(HCourseForm, self).__init__(**kwargs)

    course = forms.ModelChoiceField(queryset=self.teacher.gives_courses.all())



class HomeworkForm(forms.ModelForm):
    def __init__(self, **kwargs):
        self.course = kwargs.pop('course')
        return super(HCourseForm, self).__init__(**kwargs)

    class Meta:
        model = Homework
        fields = ('homework_type', 'content',)
