from freevle.organizer.models import *
from datetime import datetime

def make_homework(topic_abbr=None, homeworktype_abbr=None, date_format=None, date_str=None, content=None):
    topic_abbr = topic_abbr or raw_input('Topic: ')
    homeworktype_abbr = homeworktype_abbr or raw_input('Homework type: ')
    content = content or raw_input('Homework content: ')
    date_format = date_format or '%d-%m-%Y'
    date_str = date_str or raw_input('Date({}): '.format(date_format))
    due_date = datetime.strptime(date_str, date_format).date()

    it_worked = False
    hw_type = HomeworkType.objects.get(abbr=homeworktype_abbr)
    if hw_type is None:
        print 'HomeworkType not found.'
        return
    for course in Course.objects.filter(topic__abbr=topic_abbr):
        it_worked = True
        h = Homework(
            homework_type=hw_type,
            course=course,
            content=content,
            due_date=due_date
        )
        h.save()
        print 'Saved {}.'.format(h)
    if not it_worked:
        print 'No homework saved.'
