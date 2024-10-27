from django.test import TestCase

from reports.services.summaryRecord import SummaryRecord

class SummaryRecordTests(TestCase):
    def test_it_can_be_sorted_based_on_amount(self):
        records = [
            SummaryRecord(1, 'Income', 6000.00, 0.00, 0.00, 0.00, 'CZK'),
            SummaryRecord(2, 'Outcome', -5500.00, 0.00, 0.00, 0.00, 'CZK'),
            SummaryRecord(3, 'Balance', 0.00, 0.00, 0.00, 0.00, 'CZK')
        ]
        
        records = sorted(records)
        self.assertEquals(6000.00, records[0].amount)
        self.assertEquals(0.00, records[1].amount)
        self.assertEquals(-5500.00, records[2].amount)