
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
        
class RecordViewTests(TestCase):
    def test_record_view_shows_record(self):
        """
        Record View shows Form for Record
        """
        record = create_record('Newest Record', 200.00)
        url = reverse('record:edit', args=(record.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, record.description)