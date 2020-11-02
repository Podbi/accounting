class MonthSummary:
    def __init__(self, currency):
        self.currency = currency
        self.revenues = []
        self.expenses = []
        self.revenue = 0.00;
        self.expense = 0.00;
        self.summary = 0.00;
        
    def addRevenue(self, record):
        self.revenues.append(record)
        self.revenue += round(record.amount, 0)
        self.summary = self.revenue + self.expense
        
    def addExpense(self, record):
        self.expenses.append(record)
        self.expense += round(record.amount, 0)
        self.summary = self.revenue + self.expense
        
    def sort(self):
        self.revenues = sorted(self.revenues)
        self.expenses = sorted(self.expenses, reverse=True)