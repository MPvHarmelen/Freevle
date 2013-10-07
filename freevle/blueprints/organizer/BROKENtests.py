import unittest
import datetime

from freevle.testing import TestBase
from freevle import db
from .models import PeriodMeta

from sqlalchemy.exc import StatementError

class OrganizerTests(TestBase):
    def get_test_period_meta(self):
        return PeriodMeta(
            start_date=datetime.date(2013, 1, 1),
            end_date=datetime.date(2020, 1, 1),
            day_of_week=0,
            period_length=50,
            breaks_after_period=[3, 5, 7],
            break_lengths=[20, 30, 10],
            start_of_day=datetime.time(8, 25),
            min_periods=7
        )

    def test_comma_seperated_integer(self):
        pm = self.get_test_period_meta()

        # Try to put in a CommaSeperatedSomethingElse
        pm.break_lengths = ["Ceci n'est pas un int"]
        db.session.add(pm)
        self.assertRaises(StatementError, db.session.commit)
        db.session.rollback()

        # Try to put in a list that shouldn't fit.
        pm.break_lengths = [int('1'*257)]
        db.session.add(pm)
        self.assertRaises(StatementError, db.session.commit)
        db.session.rollback()

    def test_period_meta(self):
        db.session.add(self.get_test_period_meta())
        db.session.commit()
        pm_got = PeriodMeta.query.get(1)
        self.assertEquals(pm_got.start_date, datetime.date(2013, 1, 1))
        self.assertEquals(pm_got.end_date, datetime.date(2020, 1, 1))
        self.assertEquals(pm_got.day_of_week, 0)
        self.assertEquals(pm_got.period_length, 50)
        self.assertEquals(pm_got.breaks_after_period, [3, 5, 7])
        self.assertEquals(pm_got.break_lengths, [20, 30, 10])
        self.assertEquals(pm_got.start_of_day, datetime.time(8, 25))
        self.assertEquals(pm_got.min_periods, 7)


suite = unittest.makeSuite(OrganizerTests)
