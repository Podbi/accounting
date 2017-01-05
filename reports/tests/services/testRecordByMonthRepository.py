import datetime
from django.utils import timezone
from django.test import TestCase

from reports.service import RecordByMonthRepository
from reports.models import Record
from reports.models import RecordType
from reports.models import Currency
from reports.models import MoneySource

def create_record(description, money, date):
    currency = Currency.objects.create(code="CZK")
    type = RecordType.objects.create()
    source = MoneySource.objects.create()
    return Record.objects.create(description=description, date=date, money=money, currency=currency, source=source, type=type)

class RecordByMonthRepositoryTests(TestCase):
    def test_finds_all_by_dates(self):
        records = [
            create_record('First Record', 100.00, timezone.now()),
            create_record('Second Record', -300.00, timezone.now()),
            create_record('Third Record', 50.00, timezone.now()),
        ]
        
        result = RecordByMonthRepository().findAllByDates(
            datetime.date.today() + datetime.timedelta(-15),
            datetime.date.today() + datetime.timedelta(15),
            'CZK'
        )
        self.assertEquals(3, len(result))
        self._assert_record(records[0], result[0])
        self._assert_record(records[1], result[1])
        self._assert_record(records[2], result[2])
        
    def _assert_record(self, expectedRecord, actualRecord):
        self.assertEquals(expectedRecord.id, actualRecord.id)
        self.assertEquals(expectedRecord.description, actualRecord.description)
        self.assertEquals(expectedRecord.place, actualRecord.place)
        self.assertEquals(expectedRecord.type.name, actualRecord.type)
        self.assertEquals(expectedRecord.money, actualRecord.money)
        self.assertEquals(expectedRecord.currency.code, actualRecord.currency)
        self.assertEquals(expectedRecord.source.name, actualRecord.source)
        