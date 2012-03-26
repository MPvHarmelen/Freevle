import requests
import datetime
from bs4 import BeautifulSoup

from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError

from cygy.organizer import models
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

    #infoweb = raw_input('Enter the webaddress to your infoweb root (like http://example.com/infoweb/): ')
    infoweb = 'http://cygy.nl/ftp_cg/roosters/infoweb/'
    cookies = requests.get(infoweb + 'index.php').cookies

    this_week = datetime.datetime.today().isocalendar()[1]

    classes_page = requests.get('{}selectie.inc.php?wat=week&weeknummer={}&type=0'.format(infoweb, this_week), cookies=cookies)
    classes_soup = BeautifulSoup(classes_page.text)

    classes_names = []
    for option in classes_soup.find_all('option')[2:]:
        classes_names.append(option['value'])

    #classes = []
    students = []
    for cls in classes_names:
        students_page = requests.get('{}selectie.inc.php?wat=groep&weeknummer={}&type=0&groep={}'.format(infoweb, this_week, cls), cookies=cookies)
        students_soup = BeautifulSoup(students_page.text)

        #students = []
        for option in students_soup('option')[2:]:
            students.append([int(option['value']), option.string])

        #classes.append(students)

    timetables = []
    cookies = requests.get(infoweb + 'index.php').cookies
    for student in students:
        timetable_page = requests.get('{}print.php?week={}&id={}&type=0'.format(infoweb, this_week, student[0]), cookies=cookies)
        timetable_soup = BeautifulSoup(timetable_page.text)

        table = timetable_soup('table')[0]
        days = [[], [], [], [], [],]
        for tr in table('tr')[1:]:
            for i, td in enumerate(tr('td')):
                if 'class' in td.attrs:
                    data = [[], [], [],]
                else:
                    data = td.span.string.strip().split()
                days[i].append(data)
        print days

    if verbosity > 1:
        print

if DEBUG:
    post_syncdb.connect(debug_data, sender=models)

if __name__ == '__main__':
    debug_data(0, verbosity=1, interactive=1)
