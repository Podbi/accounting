import datetime
from django.utils import timezone
from django.test import TestCase

from reports.services.yearSummaryCalculator import YearSummaryCalculator
from reports.models import Record
from reports.models import RecordType
from reports.models import Currency
from reports.models import MoneySource

def create_record(description, money, date):
    currency = Currency.objects.create(code="CZK")
    source = MoneySource.objects.create()
    type = RecordType.objects.create()
    return Record.objects.create(description=description, date=date, money=money, currency=currency, source=source, type=type)

class YearSummaryCalculatorTests(TestCase):
    def test_provides_list_of_available_months(self):
        create_record('First Record', 100.00, datetime.datetime(2016, 3, 21))
        create_record('Second Record', -300.00, datetime.datetime(2017, 8, 10))
        create_record('Third Record', 50.00, datetime.datetime(2016, 11, 8))
        create_record('Fourth Record', 50.00, datetime.datetime(2015, 12, 3))
        create_record('Fourth Record', 50.00, datetime.datetime(2016, 12, 31))
                
        months = YearSummaryCalculator().listOfAvailable()
        self.assertEquals(3, len(months))
        self.assertEquals('/reports/year-summary/2015', months[0]['url'])
        self.assertEquals('2015', months[0]['label'])
        self.assertEquals('/reports/year-summary/2016', months[1]['url'])
        self.assertEquals('2016', months[1]['label'])
        self.assertEquals('/reports/year-summary/2017', months[2]['url'])
        self.assertEquals('2017', months[2]['label'])
        