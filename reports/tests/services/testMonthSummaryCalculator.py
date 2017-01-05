import datetime
from django.utils import timezone
from django.test import TestCase

from reports.services.monthSummaryCalculator import MonthSummaryCalculator
from reports.services.monthSummary import MonthSummary
from reports.services.summaryRecord import SummaryRecord
from reports.models import Record
from reports.models import RecordType
from reports.models import Currency
from reports.models import MoneySource

def create_record(description, money, date):
    currency = Currency.objects.create(code="CZK")
    source = MoneySource.objects.create()
    type = RecordType.objects.create()
    return Record.objects.create(description=description, date=date, money=money, currency=currency, source=source, type=type)

class MonthSummaryCalculatorTests(TestCase):
    def test_calculates_correctly_on_three_records(self):
        create_record('First Record', 100.00, timezone.now())
        create_record('Second Record', -300.00, timezone.now())
        create_record('Third Record', 50.00, timezone.now())
        
        summary = MonthSummaryCalculator().calculate(
            datetime.date.today() + datetime.timedelta(-15),
            datetime.date.today() + datetime.timedelta(15),
            'CZK'
        )
        self.assertIsInstance(summary, MonthSummary)
        self.assertEquals('CZK', summary.currency)
        self.assertEquals(150.00, summary.revenue)
        self.assertEquals(-300.00, summary.expense)
        self.assertEquals(2, len(summary.revenues))
        self.assertEquals(1, len(summary.expenses))
        for revenue in summary.revenues:
            self.assertIsInstance(revenue, SummaryRecord)
        for expense in summary.expenses:
            self.assertIsInstance(expense, SummaryRecord)
    
    def test_provides_list_of_available_months(self):
        create_record('First Record', 100.00, datetime.datetime(2016, 12, 21))
        create_record('Second Record', -300.00, datetime.datetime(2016, 12, 10))
        create_record('Third Record', 50.00, datetime.datetime(2016, 11, 8))
        create_record('Fourth Record', 50.00, datetime.datetime(2017, 1, 3))
        create_record('Fourth Record', 50.00, datetime.datetime(2017, 1, 1))
                
        months = MonthSummaryCalculator().listOfAvailable()
        self.assertEquals(3, len(months))
        self.assertEquals('/reports/month-summary/2016/11', months[0]['url'])
        self.assertEquals('Listopad 2016', months[0]['label'])
        self.assertEquals('/reports/month-summary/2016/12', months[1]['url'])
        self.assertEquals('Prosinec 2016', months[1]['label'])
        self.assertEquals('/reports/month-summary/2017/01', months[2]['url'])
        self.assertEquals('Leden 2017', months[2]['label'])
        