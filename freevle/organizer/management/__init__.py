import requests
import datetime
from bs4 import BeautifulSoup

from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError
from django.db import IntegrityError # Temporary!

from freevle.custom.debug.markov import Markov
from freevle.organizer import models
from freevle.users.models import UserProfile
from freevle.settings import DEBUG

class Course(object):
    def __init__(self, topic, teacher, students):
        self.topic = topic
        self.teacher = teacher
        self.students = students

    def __eq__(self, other):
        if (self.topic == other.topic and self.teacher == other.teacher and
            self.students == other.students):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<Course {} by {}>'.format(self.topic, self.teacher)


class Lesson(object):
    def __init__(self, teacher, topic, classroom, period, day):
        self.teacher = teacher
        self.topic = topic
        self.classroom = classroom
        self.period = period
        self.day = day
        self.students = []
        self.course = None
        self.lesson = models.Lesson()

    def save(self, start_date, end_date):
        day = models.DAY_CHOICES[self.day+1][0]
        self.lesson.classroom = self.classroom
        self.lesson.day_of_week = day
        self.lesson.period = self.period
        self.lesson.start_date = start_date
        self.lesson.end_date = end_date
        self.lesson.course = self.course
        self.lesson.save()

    def __eq__(self, other):
        if (self.teacher == other.teacher and self.topic == other.topic and
            self.classroom == other.classroom and
            self.period == other.period and self.day == other.day):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __repr__(self):
        return '<Lesson by {}: {} ({}.{} in {})>'.format(self.teacher,
                                                         self.topic,
                                                         self.period,
                                                         self.day,
                                                         self.classroom)


def debug_data(sender, **kwargs):
    verbosity = kwargs['verbosity']
    if verbosity > 1:
        print

    if not kwargs['interactive']:
        return
    else:
        cont = raw_input('Do you want sync with infoweb? (Y/n): ')
        if not cont.lower() in ('yes', 'y', '',):
            return

    if verbosity > 1:
        print (' Reading the complete works of William Shakespeare for'
               ' inspiration.')
    file = open('custom/debug/shakespeare.txt')
    shakespeare = Markov(file)

    #infoweb = raw_input(('Enter the webaddress to your infoweb root '
    #                     '(like http://example.com/infoweb/):'))
    infoweb = 'http://cygy.nl/ftp_cg/roosters/infoweb/'
    cookies = requests.get(infoweb + 'index.php').cookies

    this_week = datetime.datetime.today().isocalendar()[1]
    today = datetime.datetime.today()
    start_date = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    end_date = start_date + datetime.timedelta(days=7)

    url = '{}selectie.inc.php?wat=week&weeknummer={}&type=0'.format(infoweb,
                                                                    this_week)
    classes_page = requests.get(url, cookies=cookies)
    classes_soup = BeautifulSoup(classes_page.text)

    classes_names = []
    for option in classes_soup.find_all('option')[2:]:
        classes_names.append(option['value'])
        print option['value']

    students_group, created = Group.objects.get_or_create(name='students')
    teachers_group, created = Group.objects.get_or_create(name='teachers')
    students = []
    for cls in classes_names:
        url = '{}selectie.inc.php?wat=groep&weeknummer={}&type=0&groep={}'
        url = url.format(infoweb, this_week, cls)
        students_page = requests.get(url, cookies=cookies)
        students_soup = BeautifulSoup(students_page.text)

        for option in students_soup('option')[1:]:
            name = option.string
            first_name = name.split()[0]
            last_name = ' '.join(name.split()[1:])
            abbr = option['value']
            password = shakespeare.generate_markov_text(2).replace(' ', '')
            student = User(username=abbr, first_name=first_name,
                           last_name=last_name)
            student.set_password(password)
            student.save()
            class_group, created = Group.objects.get_or_create(name=cls)
            student.groups.add(class_group, students_group)
            student.save()
            profile = student.get_profile()
            profile.designation = abbr
            profile.save()

            students.append([int(option['value']), option.string, student])
            print student

        #classes.append(students)

    lessons = []
    cookies = requests.get(infoweb + 'index.php').cookies
    for student in students:
        url = '{}print.php?week={}&id={}&type=0'.format(infoweb, this_week,
                                                        student[0])
        timetable_page = requests.get(url, cookies=cookies)
        timetable_soup = BeautifulSoup(timetable_page.text)

        table = timetable_soup('table')[0]
        for period, tr in enumerate(table('tr')[1:]):
            for day, td in enumerate(tr('td')):
                if not 'class' in td.attrs:
                    options = td.span.string.strip().split()
                    teacher, topic, classroom = (options + [None] * 2)[:3]
                    try:
                        teacher = User.objects.get(username=teacher)
                    except User.DoesNotExist:
                        password = shakespeare.generate_markov_text(2)
                        password = password.replace(' ', '')
                        teacher = User(username=teacher, first_name=teacher,
                                       last_name=teacher)
                        teacher.set_password(password)
                        teacher.groups.add(teachers_group)
                        teacher.save()

                    if topic is None:
                        teacher, topic = topic, teacher.username
                        teacher, _ = User.objects.get_or_create(username='-')
                    topic = models.Topic.objects.get_or_create(name=topic,
                                                               abbr=topic)
                    topic = topic[0]

                    l = Lesson(teacher, topic, classroom, period, day)
                    print l
                    exists = False
                    for lesson in lessons:
                        if l == lesson:
                            lesson.students.append(student[2])
                            exists = True
                            break
                    if not exists:
                        l.students.append(student[2])
                        lessons.append(l)

    courses = []
    for lesson in lessons:
        for other in lessons:
            if (lesson.topic == other.topic and lesson.teacher == other.teacher
                    and lesson.students == other.students):
                if lesson.course is not None and other.course is None:
                    other.course = lesson.course
                elif lesson.course is None and other.course is not None:
                    lesson.course = other.course
                elif lesson.course is None and other.course is None:
                    course = Course(lesson.topic, lesson.teacher,
                                    lesson.students)
                    for othercourse in courses:
                        if course == othercourse:
                            course = othercourse
                            break
                    lesson.course = course
                    other.course = course
                    courses.append(course)
                    print course, course.students

    for course in courses:
        coursemodel = models.Course(topic=course.topic,
                                    teacher=course.teacher)
        coursemodel.save()
        coursemodel.students.add(*course.students)
        for lesson in lessons:
            if lesson.course == course:
                lesson.course = coursemodel

    for lesson in lessons:
        if lesson.classroom is None:
            lesson.classroom = '-'
        lesson.save(start_date, end_date)

    if verbosity > 1:
        print

if DEBUG:
    post_syncdb.connect(debug_data, sender=models)

if __name__ == '__main__':
    debug_data(0, verbosity=1, interactive=1)
