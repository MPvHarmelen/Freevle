from freevle.organizer.models import *
import datetime
today = datetime.date.today() + datetime.timedelta(days=1)

def lesson_save(lesson, type):
    hw = HomeworkType.objects.filter(abbr=type)[0]
    l = Lesson.objects.filter(course__topic__abbr = lesson)
    for les in l:
        attr = {
            'due_date':today,
            'homework_type':hw,
            'lesson':les,
            'content':'je lul(t)',
        }
        Homework(**attr).save()