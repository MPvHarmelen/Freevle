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


class Lesson(object):
    def __init__(self, teacher, topic, classroom, period, day):
        self.teacher = teacher
        self.topic = topic
        self.classroom = classroom
        self.period = period
        self.day = day
        self.students = []
        self.course = None

    def save(self, start_date, end_date):
        day = models.DAY_CHOICES[self.day+1]
        self.lesson = models.Lesson(classroom=self.teacher, day_of_week=day,
                                    start_date=start_date, end_date=end_date)
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
    print start_date, end_date

    url = '{}selectie.inc.php?wat=week&weeknummer={}&type=0'.format(infoweb,
                                                                    this_week)
    classes_page = requests.get(url, cookies=cookies)
    classes_soup = BeautifulSoup(classes_page.text)

    classes_names = []
    for option in classes_soup.find_all('option')[2:]:
        classes_names.append(option['value'])
        print option['value']
    classes_names = [classes_names[0]]

    students_group, created = Group.objects.get_or_create(name='students')
    students = []
    for cls in classes_names:
        url = '{}selectie.inc.php?wat=groep&weeknummer={}&type=0&groep={}'
        url = url.format(infoweb, this_week, cls)
        students_page = requests.get(url, cookies=cookies)
        students_soup = BeautifulSoup(students_page.text)

        for option in students_soup('option')[2:]:
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

    students = students[:3]

    lessons = []
    cookies = requests.get(infoweb + 'index.php').cookies
    for student in students:
        url = '{}print.php?week={}&id={}&type=0'.format(infoweb, this_week,
                                                        student[0])
        timetable_page = requests.get(url, cookies=cookies)
        timetable_soup = BeautifulSoup(timetable_page.text)

        table = timetable_soup('table')[0]
        for day, tr in enumerate(table('tr')[1:]):
            for period, td in enumerate(tr('td')):
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
                        teacher.save()

                    try:
                        topic = models.Topic.objects.get_or_create(name=topic,
                                                                   abbr=topic)
                        topic = topic[0]
                    except IntegrityError:
                        topic = None

                    l = Lesson(teacher, topic, classroom, period, day)
                    exists = False
                    for lesson in lessons:
                        if l == lesson:
                            print student
                            lesson.students.append(student[2])
                            exists = True
                            break
                    if not exists:
                        l.students.append(student[2])
                        lessons.append(l)
                    l.save(start_date, end_date)

    for lesson in lessons:
        for other in lessons:
            if (lesson.topic == other.topic and lesson.teacher == other.teacher
                    and lesson.students == other.students):
                if lesson.course is not None and other.course is None:
                    other.course = lesson.course
                elif lesson.course is None and other.course is not None:
                    lesson.course = other.course
                elif lesson.course is None and other.course is None:
                    try:
                        print lesson.topic, lesson.teacher, lesson.students
                        course = models.Course.objects.get_or_create(
                            topic=lesson.topic,
                            teacher=lesson.teacher,
                        )
                        course.students.add(*[i[2] for i in lesson.students])
                    except IntegrityError:
                        # Need to fix this for lessons without enough
                        # data.
                        course = None
                    lesson.lesson.course = course
                    lesson.lesson.save()
                    other.lesson.course = course
                    other.lesson.save()


                print course

    if verbosity > 1:
        print

if DEBUG:
    post_syncdb.connect(debug_data, sender=models)

if __name__ == '__main__':
    debug_data(0, verbosity=1, interactive=1)
