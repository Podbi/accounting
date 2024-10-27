from django.test import TestCase

from reports.services.monthSummary import MonthSummary
from reports.services.summaryRecord import SummaryRecord

class MonthSummaryTests(TestCase):
    def test_it_provides_currency_given_in_constructor(self):
        self.assertEquals('CZK', MonthSummary('CZK').currency)
    
    def test_it_calculates_revenue_correctly(self):
        summary = MonthSummary('CZK')
        summary.addRevenue(SummaryRecord(1, 'Income', 300.00, 50.00, 150.00, 100.00, 'CZK'))
        summary.addRevenue(SummaryRecord(2, 'Payment', 600.00, 200.00, 100.00, 300.00, 'CZK'))
        summary.addRevenue(SummaryRecord(3, 'Bonus', 2000.00, 1500.00, 300.00, 200.00, 'CZK'))
        summary.sort()
        
        self.assertEquals(2900.00, summary.revenue)
        self.assertEquals(3, len(summary.revenues))
        self.assertEquals('Bonus', summary.revenues[0].name)
        self.assertEquals(2000.00, summary.revenues[0].amount)
        self.assertEquals('Payment', summary.revenues[1].name)
        self.assertEquals(600.00, summary.revenues[1].amount)
        self.assertEquals('Income', summary.revenues[2].name)
        self.assertEquals(300.00, summary.revenues[2].amount)
        self.assertEquals(1750.00, summary.categorized_revenue[MonthSummary.NECESSITY])
        self.assertEquals(550.00, summary.categorized_revenue[MonthSummary.NICE])
        self.assertEquals(600.00, summary.categorized_revenue[MonthSummary.SAVING])
        self.assertEquals(1750.00, summary.categorized_summary[MonthSummary.NECESSITY])
        self.assertEquals(550.00, summary.categorized_summary[MonthSummary.NICE])
        self.assertEquals(600.00, summary.categorized_summary[MonthSummary.SAVING])
    
    def test_it_calculates_expense_correctly(self):
        summary = MonthSummary('CZK')
        summary.addExpense(SummaryRecord(1, 'Outcome', -600.00, -400.00, -200.00, 0.00, 'CZK'))
        summary.addExpense(SummaryRecord(2, 'Payment', -3650.00, -3050.00, -500.00, -100.00, 'CZK'))
        summary.addExpense(SummaryRecord(3, 'Wife', -5560.00, -4560.00, -900.00, -100.00, 'CZK'))
        summary.sort()
        
        self.assertEquals(-9810.00, summary.expense)
        self.assertEquals(3, len(summary.expenses))
        self.assertEquals('Wife', summary.expenses[0].name)
        self.assertEquals(-5560.00, summary.expenses[0].amount)
        self.assertEquals('Payment', summary.expenses[1].name)
        self.assertEquals(-3650.00, summary.expenses[1].amount)
        self.assertEquals('Outcome', summary.expenses[2].name)
        self.assertEquals(-600.00, summary.expenses[2].amount)
        self.assertEquals(-8010.00, summary.categorized_expense[MonthSummary.NECESSITY])
        self.assertEquals(-1600.00, summary.categorized_expense[MonthSummary.NICE])
        self.assertEquals(-200.00, summary.categorized_expense[MonthSummary.SAVING])
        self.assertEquals(-8010.00, summary.categorized_summary[MonthSummary.NECESSITY])
        self.assertEquals(-1600.00, summary.categorized_summary[MonthSummary.NICE])
        self.assertEquals(-200.00, summary.categorized_summary[MonthSummary.SAVING])
    
    def test_it_calculates_summary_correctly(self):
        summary = MonthSummary('CZK')
        summary.addRevenue(SummaryRecord(1, 'Income', 300.00, 0.00, 0.00, 0.00, 'CZK'))
        summary.addRevenue(SummaryRecord(2, 'Payment', 600.00, 0.00, 0.00, 0.00, 'CZK'))
        summary.addRevenue(SummaryRecord(3, 'Bonus', 2000.00, 0.00, 0.00, 0.00, 'CZK'))
        summary.addExpense(SummaryRecord(1, 'Outcome', -600.00, 0.00, 0.00, 0.00, 'CZK'))
        summary.addExpense(SummaryRecord(2, 'Payment', -3650.00, 0.00, 0.00, 0.00, 'CZK'))
        summary.addExpense(SummaryRecord(3, 'Wife', -5560.00, 0.00, 0.00, 0.00, 'CZK'))
        summary.sort()
        
        self.assertEquals(-6910.00, summary.summary)
