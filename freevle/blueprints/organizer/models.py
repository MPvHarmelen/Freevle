import datetime

from freevle import db
from freevle.utils.database import validate_slug
from .database import CommaSeperatedInteger, validate_day_of_week
from .database import validate_start_date, validate_end_date

from ..user.models import User

# days of week are defined according to datetime %w and  format.
DAY_DICT = {
    0 : 'Sunday',
    1 : 'Monday',
    2 : 'Tuesday',
    3 : 'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday',
}

NAME_LENGTH = 32
ABBREVIATION_LENGTH = 4
CLASSROOM_NAME_LENGTH = 16
MAX_STRING_LENGTH = 255
HEX_COLOUR_CODE_LENGTH = 7
DATE_FORMAT = '%d-%m-%Y'
TIME_FORMAT = '%H:%M'
ANNOUNCEMENT_CONTENT_SLICE = 30

class Topic(db.Model):
    """
    A topic

    Like: maths, physics, history, etc...

    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LENGTH), unique=True, nullable=False)
    abbreviation = db.Column(db.String(ABBREVIATION_LENGTH), unique=True,
                             nullable=False)

    def __repr__(self):
        return '({}) {}'.format(self.id, self.name)

course_student = db.Table('course_student',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

course_teacher = db.Table('course_teacher',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Course(db.Model):
    """A group of students with a teacher and a topic."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LENGTH), unique=True, nullable=False)
    slug = db.Column(db.String(NAME_LENGTH), unique=True, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship(Topic,
                            backref=db.backref('courses',
                                               order_by='Course.id',
                                               lazy='dynamic')
    )
    teachers = db.relationship(User,
                              secondary=course_teacher,
                              order_by=User.id,
                              lazy='dynamic',
                              backref=db.backref('gives_courses',
                                                 order_by='Course.id',
                                                 lazy='dynamic')
    )
    #    limit_choices_to={'groups__name': 'teachers'}

    students = db.relationship(User,
                               secondary=course_student,
                               order_by=User.id,
                               lazy='dynamic',
                               backref=db.backref('takes_courses',
                                                  order_by='Course.id',
                                                  lazy='dynamic')
    )
#        limit_choices_to={'groups__name': 'students'}

    validate_slug = db.validates('slug')(validate_slug)

    def __repr__(self):
        teachers = ', '.join(teacher.designation for teacher in self.teacher.all())
        return '({}) {} ({} {})'.format(self.id, self.name, self.topic, teachers)

class Classroom(db.Model):
    """A classroom"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(CLASSROOM_NAME_LENGTH), unique=True,
                     nullable=False)

    validate_name = db.validates('name')(validate_slug)

    def __repr__(self):
        return '({}) {}'.format(self.id, self.name)

class TimeSlot(db.Model):
    """Time slot in a weekly timetable."""
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)

    validate_day_of_week = db.validates('day_of_week')(validate_day_of_week)

    def get_duration(self, date):
        """Get the duration for this time slot that is applicable at <date>."""
        start_time = end_time = None
        return start_time, end_time

    def __repr__(self):
        return '({}) {} {}'.format(self.id, DAY_DICT[self.day_of_week],
                                   self.period)

class TimeSlotDuration(db.Model):
    """Duration of a timeslot"""
    id = db.Column(db.Integer, primary_key=True)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'),
                             nullable=False)
    time_slot = db.relationship(TimeSlot,
                                backref=db.backref('durations',
                                                   order_by='TimeSlotDuration.id',
                                                   lazy='dynamic')
    )

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    validate_start_date = db.validates('start_date')(validate_start_date)
    validate_end_date = db.validates('end_date')(validate_end_date)

    @db.validates('start_time')
    def validate_start_time(self, key, value):
        if getattr(self, 'end_time', None) is not None and self.end_time < value:
            raise ValueError('start_time should not be after end_time.')
        else:
            return value

    @db.validates('end_time')
    def validate_end_time(self, key, value):
        if getattr(self, 'start_time', None) is not None and value < self.start_time:
            raise ValueError('end_time should not be before start_time.')
        else:
            return value

    def __repr__(self):
        return '({}) {} - {} ({} - {})'.format(
            self.id,
            self.start_time.strftime(TIME_FORMAT),
            self.end_time.strftime(TIME_FORMAT),
            self.start_date.strftime(DATE_FORMAT),
            self.end_date.strftime(DATE_FORMAT)
        )


class Lesson(db.Model):
    """Time and place a course is given."""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship(Course,
                             backref=db.backref('lessons',
                                                order_by='Lesson.id',
                                                lazy='dynamic')
    )

    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'),
                             nullable=False)
    classroom = db.relationship(Classroom,
                                backref=db.backref('lessons',
                                                   order_by='Lesson.id',
                                                   lazy='dynamic')
    )

    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'),
                             nullable=False)
    time_slot = db.relationship(TimeSlot,
                                backref=db.backref('lessons',
                                                   order_by='Lesson.id',
                                                   lazy='dynamic')
    )

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    validate_start_date = db.validates('start_date')(validate_start_date)
    validate_end_date = db.validates('end_date')(validate_end_date)

    __table_args__ = (
        db.UniqueConstraint('course_id','time_slot_id'),
    )

    def __repr__(self):
        return '{} {} {}'.format(self.course.topic, DAY_DICT[self.day_of_week],
                                 self.period)

class HomeworkCategory(db.Model):
    """
    A type of homework

    Like: exam, test, small test, oral exam, etc...

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_LENGTH), unique=True, nullable=False)
    abbreviation = db.Column(db.String(ABBREVIATION_LENGTH), nullable=False)
    colour = db.Column(db.String(HEX_COLOUR_CODE_LENGTH), nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    #help_text=_('Homework with a weight higher ')
    #            'than 10 will appear under '
    #            '`comming homework`')

    @db.validates('colour')
    def validate_hex_colour(self, key, value):
        if re.match('^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
            return value
        else:
            raise ValueError('This is an invalid color code. It must be a html '
                             'hex color code e.g. #000000')

#    def __cmp__(self, other):
#        return cmp(self.weight, other.weight)
#
#    def __eq__(self, other):
#        if type(self) == type(other):
#            return self.id == other.id
#        return False

    def __repr__(self):
        return self.name

class Homework(db.Model):
    """
    Homework

    For instance: history test on Friday the thirteenth

    """
    id = db.Column(db.Integer, primary_key=True)

    homework_category_id = db.Column(db.Integer,
                                     db.ForeignKey('homework_category.id'),
                                     nullable=False)
    homework_category = db.relationship(
        HomeworkCategory,
        backref=db.backref('homework',
                           order_by='Homework.id',
                           lazy='dynamic')
    )

    content = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship(Course,
                             backref=db.backref('homework',
                                                order_by='Homework.id',
                                                lazy='dynamic')
    )

    due_date = db.Column(db.Date, nullable=False)
    period = db.Column(db.Integer)

#    def __eq__(self, other):
#        if type(self) == type(other):
#            def extended_and(li):
#                if len(li) > 1:
#                    return li.pop() and extended_and(li)
#                else:
#                    return li[0]
#            attrs = ['homework_category', 'content', 'course', 'due_date', 'period']
#            return extended_and(getattr(self, attr) == getattr(other, attr) for
#                                attr in attrs)
#        else:
#            return False

    def __repr__(self):
        return '{} {} on {}'.format(self.course.topic, self.homework_category,
                                    self.due_date.strftime(DATE_FORMAT))

lesson_modification_teacher = db.Table('lesson_modification_teacher',
    db.Column('lesson_modification_id', db.Integer,
              db.ForeignKey('lesson_modification.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)

class LessonModification(db.Model):
    """
    Temporary changes for a lesson

    This is useful for when a teacher is ill or when a classroom is unusable and
    you would want a replacement or you would want to move the lesson to another
    timeslot and/or week.

    """
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    lesson = db.relationship(Lesson,
                             backref=db.backref('changed',
                                                order_by='LessonModification.id',
                                                lazy='dynamic')
    )

    week = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    new_week = db.Column(db.Integer)
    new_year = db.Column(db.Integer)
    new_teacher = db.relationship(
        User,
         secondary='lesson_modification_teacher',
         order_by=User.id,
         backref=db.backref('changed_lessons',
                            order_by='LessonModification.id',
                            lazy='dynamic')
    )
#        limit_choices_to={'groups__name':'teachers'}
    new_classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    new_classroom = db.relationship(
        Classroom,
        backref=db.backref('changed_lessons',
                           order_by='LessonModification.id',
                           lazy='dynamic')
    )

    new_time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'))
    new_time_slot = db.relationship(
        TimeSlot,
        backref=db.backref('lesson_modifcations',
                           order_by='LessonModification.id',
                           lazy='dynamic')
    )


    __table_args__ = (
        db.UniqueConstraint('lesson_id', 'week', 'year'),
    )

    def __repr__(self):
        return 'Modification of {} in week {}, {}'.format(self.lesson,
                                                          self.week,
                                                          self.year)


class TeacherCancellationTime(db.Model):
    """Timespan a teacher is not able to teach."""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher = db.relationship(
        User,
        backref=db.backref('cancelled',
                           order_by='TeacherCancellationTime.id',
                           lazy='dynamic')
    )
#        limit_choices_to={'groups__name':'teachers'},

    start_date = db.Column(db.Date, nullable=False)
    start_period = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    end_period = db.Column(db.Integer, nullable=False)

    validate_start_date = db.validates('start_date')(validate_start_date)
    validate_end_date = db.validates('end_date')(validate_end_date)

    @db.validates('start_period')
    def validate_start_period(self, key, value):
        if getattr(self, 'end_period', None) is not None and \
            self.end_period < value:
            raise ValueError('start_period should not be after end_period.')
        else:
            return value

    @db.validates('end_period')
    def validate_end_period(self, key, value):
        if getattr(self, 'start_period', None) is not None and \
            value < self.start_period:
            raise ValueError('end_period should not be before start_period.')
        else:
            return value

    def __repr__(self):
        return '({}) cancellation of {} ({} - {})'.format(
            self.teacher,
            self.start_date.strftime(DATE_FORMAT),
            self.end_date.strftime(DATE_FORMAT)
        )

class ClassroomCancellationTime(db.Model):
    """Timespan a classroom is out of order."""
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'),
                             nullable=False)
    classroom = db.relationship(
        Classroom,
        backref=db.backref('cancelled',
                           order_by='ClassroomCancellationTime.id',
                           lazy='dynamic')
    )

    start_date = db.Column(db.Date, nullable=False)
    start_period = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    end_period = db.Column(db.Integer, nullable=False)

    validate_start_date = db.validates('start_date')(validate_start_date)
    validate_end_date = db.validates('end_date')(validate_end_date)

    def __repr__(self):
        return '({}) cancellation of {} ({} - {})'.format(
            self.id,
            self.classroom,
            self.start_date.strftime(DATE_FORMAT),
            self.end_date.strftime(DATE_FORMAT)
        )

class Announcement(db.Model):
    """Announcement to be shown next to the timetable."""
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    content = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)

    validate_start_date = db.validates('start_date')(validate_start_date)
    validate_end_date = db.validates('end_date')(validate_end_date)

    def __repr__(self):
        return '({}) {}... ({} - {})'.format(
            self.id,
            self.content[:ANNOUNCEMENT_CONTENT_SLICE],
            self.start_date.strftime(DATE_FORMAT),
            self.end_date.strftime(DATE_FORMAT)
        )

