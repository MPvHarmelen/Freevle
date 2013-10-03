import datetime
import requests
from bs4 import BeautifulSoup

week_n = str(datetime.date.today().isocalendar()[1])
base_url = 'http://www.cygnusgymnasium.nl/ftp_cg/roosters/infoweb/'

cookie_url = '{0}index.php'.format(base_url)
r = requests.get(cookie_url)
cookies = r.cookies



def get_groups():
    group_url = '{0}selectie.inc.php?wat=week&weeknummer={1}'.format(base_url, week_n)
    group_result = requests.get(group_url, cookies=cookies)
    group_soup = BeautifulSoup(group_result.text)
    group_options = group_soup.find_all('option')

    groups = []

    for option in group_options:
        group = option.string
        if group.isalnum():
            groups.append(group)

    return groups



def get_students(groups):
    students = []

    for group in groups:
        student_url = '{0}selectie.inc.php?wat=groep&weeknummer={1}&groep={2}'.format(base_url, week_n, group)
        student_result = requests.get(student_url, cookies=cookies)
        student_soup = BeautifulSoup(student_result.text)
        student_options = student_soup.find_all('option')

        for option in student_options:
            llnr = option['value']

            if llnr.isalnum():
                name = option.string

                students.append([2, llnr, name, group])

    return students



def get_teachers():
    teacher_url = '{0}selectie.inc.php?wat=groep&weeknummer={1}&groep=*allen&type=1'.format(base_url, week_n)
    teacher_result = requests.get(teacher_url, cookies=cookies)
    teacher_soup = BeautifulSoup(teacher_result.text)
    teacher_options = teacher_soup.find_all('option')

    teachers = []

    for option in teacher_options:
        abbrev = option.string

        if abbrev.isalnum():
            teachers.append([3, abbrev])

    return teachers


if __name__ == '__main__':
    users = get_students(get_groups()) + get_teachers()
    print(users)
