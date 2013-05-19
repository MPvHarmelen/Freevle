from freevle.organizer.models import *
from datetime import datetime

def make_homework(course_abbr=None, homeworktype_abbr=None, date_format=None, date_str=None, content=None):
    course_abbr = course_abbr or raw_input('Course: ')
    homeworktype_abbr = homeworktype_abbr or raw_input('Homework type: ')
    content = content or raw_input('Homework content: ')
    date_format = date_format or '%d-%m-%Y'
    date_str = date_str or raw_input('Date({}): '.format(date_format))
    due_date = datetime.strptime(date_str, date_format).date()
    for lesson in Lesson.objects.filter(course__topic__abbr=course_abbr):
        if lesson.day_of_week == int(due_date.strftime('%w')):
            Homework(
                homework_type=HomeworkType.objects.get(abbr=homeworktype_abbr),
                lesson=lesson,
                content=content,
                due_date=due_date
            ).save()
            print 'Homework saved.'
        else:
            print 'Not the right date.'