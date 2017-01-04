from datetime import date
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from reports.models import Record
from reports.models import RecordType
from reports.models import Currency
from reports.models import MoneySource

def create_record(description, money):
    currency = Currency.objects.create(code="CZK")
    source = MoneySource.objects.create()
    type = RecordType.objects.create()
    return Record.objects.create(description=description, date=timezone.now(), money=money, currency=currency, source=source, type=type)
        
class RecordIndexViewTests(TestCase):
    def test_index_view_shows_latest_records(self):
        """
        View Action is accessible
        """
        response = self.client.get(reverse('record:index'))
        self.assertEquals(response.status_code, 200)

    def test_index_view_shows_latest_record_on_record_created(self):
        """
        View Action shows added latest record
        """
        create_record('Record 01', 100.00)
        response = self.client.get(reverse('record:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['records'], ['<Record: %s - Record 01 za 100.0 CZK>' % timezone.now().strftime('%d.%m.%Y')])
     