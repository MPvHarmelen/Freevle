import datetime
from freevle import db
from .database import CommaSeperatedInteger
DAY_DICT = {
    0 : 'Sunday',
    1 : 'Monday',
    2 : 'Tuesday',
    3 : 'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday',
}

class PeriodMeta(db.Model):
    """
    Defines the length of periods and more

    Defines the length of periods, the number of breaks and their lengths, the
    startting time of a day and the minumum number of periods shown in the
    timetable view.

    """

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)

    period_length = db.Column(db.Integer, nullable=False)
    breaks_after_period = db.Column(CommaSeperatedInteger(32), nullable=False)
    break_lengths = db.Column(CommaSeperatedInteger(32), nullable=False)
    start_of_day = db.Column(db.Time, nullable=False)
    min_periods = db.Column(db.Integer, nullable=False)

    @db.validates('start_date')
    def validate_start_date(self, key, value):
        if getattr(self, 'end_date', None) is not None and self.end_date < value:
            raise ValueError('start_date should not be after end_date.')
        else:
            return value

    @db.validates('end_date')
    def validate_end_date(self, key, value):
        if getattr(self, 'start_date', None) is not None and value < self.start_date:
            raise ValueError('end_date should not be before start_date.')
        else:
            return value

    @db.validates('day_of_week')
    def validate_day_of_week(self, key, value):
        if 0 <= value <= 6:
            return value
        else:
            raise ValueError('day_of_week must lie in the interval [0,6]')

    def __repr__(self):
        return '{} ({} - {})'.format(DAY_DICT[self.day_of_week], self.start_date,
                                     self.end_date)
