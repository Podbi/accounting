from django.test import TestCase

from reports.service import DateFactory

class DateFactoryTests(TestCase):
    def test_it_creates_first_day_of_month_for_august(self):
        date = DateFactory().createFirstDayOfMonth(8, 2017)
        self.assertEquals('01.08.2017', date.strftime('%d.%m.%Y'))

    def test_it_creates_last_day_of_month_for_february(self):
        date = DateFactory().createLastDayOfMonth(2, 2016)
        self.assertEquals('29.02.2016', date.strftime('%d.%m.%Y'))
        