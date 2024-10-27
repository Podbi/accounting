from datetime import date
from django.test import TestCase

from reports.models import Record
from reports.models import RecordCategory
from reports.models import RecordType
from reports.models import Currency

class RecordMethodTests(TestCase):
    def test_record_can_display_its_data_converted_to_string(self):
        """
        Record should be able to display basic information converted to string
        """
        currency = Currency(code="CZK")
        category = RecordCategory(name="Nutný")
        record = Record(date=date(2016, 1, 10),description="Description",money=100.00,currency=currency,category=category);
        self.assertEquals('10.01.2016 - Description za 100.0 CZK (Nutný)', str(record))
        
    def test_record_can_be_displayed_even_when_it_is_empty(self):
        """
        Record should be able to be converted to string even if it is empty
        """
        record = Record(currency=Currency())
        self.assertEquals(' -  za  ', str(record))