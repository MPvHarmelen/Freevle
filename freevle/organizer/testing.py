from freevle.organizer.models import *
from datetime import datetime

def make_homework(course_abbr=None, homeworktype_abbr=None, date_format=None, date_str=None, content=None):
    course_abbr = course_abbr or input('Course: ')
    homeworktype_abbr = homeworktype_abbr or input('Homework type: ')
    content = content or input('Homework content: ')
    date_format = date_format or '%d-%m-%Y'
    date_str = date_str or input('Date({}): '.format(date_format))
    for lesson in Lesson.objects.filter(course__topic__abbr=course_abbr):
        Homework(
            homework_type=HomeworkType.objects.get(abbr=homeworktype_abbr),
            lesson=lesson,
            content=content,
            due_date=datetime.strptime(date_str, date_format)
        ).save()