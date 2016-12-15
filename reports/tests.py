
from datetime import date
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from .models import Record
from .models import RecordType
from .models import Currency
from .models import MoneySource

def create_record(description, money):
    currency = Currency.objects.create(code="CZK")
    source = MoneySource.objects.create()
    type = RecordType.objects.create()
    return Record.objects.create(description=description, date=timezone.now(), money=money, currency=currency, source=source, type=type)
        

class RecordMethodTests(TestCase):
    def test_record_can_display_its_data_converted_to_string(self):
        """
        Record should be able to display basic information converted to string
        """
        currency = Currency(code="CZK")
        record = Record(date=date(2016, 1, 10),description="Description",money=100.00,currency=currency);
        self.assertEquals('10.01.2016 - Description za 100.0 CZK', str(record))
        
    def test_record_can_be_displayed_even_when_it_is_empty(self):
        """
        Record should be able to be converted to string even if it is empty
        """
        record = Record(currency=Currency())
        self.assertEquals(' -  za  ', str(record))
        
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
        self.assertQuerysetEqual(response.context['latest_record_list'], ['<Record: %s - Record 01 za 100.0 CZK>' % timezone.now().strftime('%d.%m.%Y')])
        
class RecordViewTests(TestCase):
    def test_record_view_shows_record(self):
        """
        Record View shows Form for Record
        """
        record = create_record('Newest Record', 200.00)
        url = reverse('record:record', args=(record.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, record.description)