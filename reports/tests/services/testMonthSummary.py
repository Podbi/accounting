from django.test import TestCase

from reports.services.monthSummary import MonthSummary
from reports.services.summaryRecord import SummaryRecord

class MonthSummaryTests(TestCase):
    def test_it_provides_currency_given_in_constructor(self):
        self.assertEquals('CZK', MonthSummary('CZK').currency)
    
    def test_it_calculates_revenue_correctly(self):
        summary = MonthSummary('CZK')
        summary.addRevenue(SummaryRecord(1, 'Income', 300.00, 'CZK'))
        summary.addRevenue(SummaryRecord(2, 'Payment', 600.00, 'CZK'))
        summary.addRevenue(SummaryRecord(3, 'Bonus', 2000.00, 'CZK'))
        summary.sort()
        
        self.assertEquals(2900.00, summary.revenue)
        self.assertEquals(3, len(summary.revenues))
        self.assertEquals('Bonus', summary.revenues[0].name)
        self.assertEquals(2000.00, summary.revenues[0].amount)
        self.assertEquals('Payment', summary.revenues[1].name)
        self.assertEquals(600.00, summary.revenues[1].amount)
        self.assertEquals('Income', summary.revenues[2].name)
        self.assertEquals(300.00, summary.revenues[2].amount)
    
    def test_it_calculates_expense_correctly(self):
        summary = MonthSummary('CZK')
        summary.addExpense(SummaryRecord(1, 'Outcome', -600.00, 'CZK'))
        summary.addExpense(SummaryRecord(2, 'Payment', -3650.00, 'CZK'))
        summary.addExpense(SummaryRecord(3, 'Wife', -5560.00, 'CZK'))
        summary.sort()
        
        self.assertEquals(-9810.00, summary.expense)
        self.assertEquals(3, len(summary.expenses))
        self.assertEquals('Wife', summary.expenses[0].name)
        self.assertEquals(-5560.00, summary.expenses[0].amount)
        self.assertEquals('Payment', summary.expenses[1].name)
        self.assertEquals(-3650.00, summary.expenses[1].amount)
        self.assertEquals('Outcome', summary.expenses[2].name)
        self.assertEquals(-600.00, summary.expenses[2].amount)
    
    def test_it_calculates_summaryy_correctly(self):
        summary = MonthSummary('CZK')
        summary.addRevenue(SummaryRecord(1, 'Income', 300.00, 'CZK'))
        summary.addRevenue(SummaryRecord(2, 'Payment', 600.00, 'CZK'))
        summary.addRevenue(SummaryRecord(3, 'Bonus', 2000.00, 'CZK'))
        summary.addExpense(SummaryRecord(1, 'Outcome', -600.00, 'CZK'))
        summary.addExpense(SummaryRecord(2, 'Payment', -3650.00, 'CZK'))
        summary.addExpense(SummaryRecord(3, 'Wife', -5560.00, 'CZK'))
        summary.sort()
        
        self.assertEquals(-6910.00, summary.summary)
