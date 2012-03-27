import requests
import datetime
from bs4 import BeautifulSoup

from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError

from cygy.custom.debug.markov import Markov
from cygy.organizer import models
from cygy.users.models import UserProfile
from cygy.settings import DEBUG

def debug_data(sender, **kwargs):
    verbosity = kwargs['verbosity']
    if verbosity > 1:
        print

    if not kwargs['interactive']:
        return
    else:
        cont = raw_input('Do you want sync with infoweb?  (Y/n): ')
        if not cont.lower() in ('yes', 'y', '',):
            return

    if verbosity > 1:
        print ' Reading the complete works of William Shakespeare for inspiration.'
    file = open('custom/debug/shakespeare.txt')
    shakespeare = Markov(file)

    #infoweb = raw_input(('Enter the webaddress to your infoweb root '
    #                     '(like http://example.com/infoweb/):'))
    infoweb = 'http://cygy.nl/ftp_cg/roosters/infoweb/'
    cookies = requests.get(infoweb + 'index.php').cookies

    this_week = datetime.datetime.today().isocalendar()[1]

    url = '{}selectie.inc.php?wat=week&weeknummer={}&type=0'.format(infoweb, this_week)
    classes_page = requests.get(url, cookies=cookies)
    classes_soup = BeautifulSoup(classes_page.text)

    classes_names = []
    for option in classes_soup.find_all('option')[2:]:
        classes_names.append(option['value'])

    students_group, created = Group.objects.get_or_create(name='students')
    students = []
    for cls in classes_names:
        url = '{}selectie.inc.php?wat=groep&weeknummer={}&type=0&groep={}'.format(infoweb, this_week, cls)
        students_page = requests.get(url, cookies=cookies)
        students_soup = BeautifulSoup(students_page.text)

        for option in students_soup('option')[2:]:
            name = option.string
            first_name = name.split()[0]
            last_name = ' '.join(name.split()[1:])
            abbr = option['value']
            password = shakespeare.generate_markov_text(2).replace(' ', '')
            student = User(username=abbr, first_name=first_name, last_name=last_name)
            student.set_password(password)
            student.save()
            class_group, created = Group.objects.get_or_create(name=cls)
            student.groups.add(class_group, students_group)
            student.save()
            profile = student.get_profile()
            profile.designation = abbr
            profile.save()

            students.append([int(option['value']), option.string])

        #classes.append(students)

    timetables = []
    cookies = requests.get(infoweb + 'index.php').cookies
    for student in students:
        url = '{}print.php?week={}&id={}&type=0'.format(infoweb, this_week, student[0])
        timetable_page = requests.get(url, cookies=cookies)
        timetable_soup = BeautifulSoup(timetable_page.text)

        table = timetable_soup('table')[0]
        days = [[], [], [], [], [],]
        for tr in table('tr')[1:]:
            for i, td in enumerate(tr('td')):
                if 'class' in td.attrs:
                    data = [[], [], [],]
                else:
                    teacher, topic, classroom = td.span.string.strip().split()
                    try:
                        teacher = User.objects.get(username=teacher)
                    except User.DoesNotExist:
                        password = shakespeare.generate_markov_text(2).replace(' ', '')
                        teacher = User(username=teacher, first_name=teacher, last_name=teacher)
                        teacher.set_password(password)
                        teacher.save()
                days[i].append(data)

    if verbosity > 1:
        print

if DEBUG:
    post_syncdb.connect(debug_data, sender=models)

if __name__ == '__main__':
    debug_data(0, verbosity=1, interactive=1)
