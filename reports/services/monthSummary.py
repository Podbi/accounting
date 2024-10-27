class MonthSummary:

    NECESSITY = "necessity"
    NICE = "nice"
    SAVING = "saving"


    def __init__(self, currency):
        self.currency = currency
        self.revenues = []
        self.expenses = []
        self.revenue = 0.00
        self.expense = 0.00
        self.summary = 0.00
        self.categorized_revenue = {
            MonthSummary.NECESSITY : 0.00,
            MonthSummary.NICE : 0.00,
            MonthSummary.SAVING : 0.00
        }
        self.categorized_expense = {
            MonthSummary.NECESSITY : 0.00,
            MonthSummary.NICE : 0.00,
            MonthSummary.SAVING : 0.00

        }
        self.categorized_summary = {
            MonthSummary.NECESSITY : 0.00,
            MonthSummary.NICE : 0.00,
            MonthSummary.SAVING : 0.00
        }
        
    def addRevenue(self, record):
        self.revenues.append(record)
        self.revenue += round(record.amount, 0)

        self.categorized_revenue[MonthSummary.NECESSITY] += round(record.necessity_amount, 0) if record.necessity_amount is not None else 0.00
        self.categorized_revenue[MonthSummary.NICE] += round(record.nice_amount, 0) if record.nice_amount is not None else 0.00
        self.categorized_revenue[MonthSummary.SAVING] += round(record.saving_amount, 0)if record.saving_amount is not None else 0.00

        self._recalculateCategorizedSummary()

        self.summary = self.revenue + self.expense
        
    def addExpense(self, record):
        self.expenses.append(record)
        self.expense += round(record.amount, 0)

        self.categorized_expense[MonthSummary.NECESSITY] += round(record.necessity_amount, 0) if record.necessity_amount is not None else 0.00
        self.categorized_expense[MonthSummary.NICE] += round(record.nice_amount, 0) if record.nice_amount is not None else 0.00
        self.categorized_expense[MonthSummary.SAVING] += round(record.saving_amount, 0)if record.saving_amount is not None else 0.00

        self._recalculateCategorizedSummary()

        self.summary = self.revenue + self.expense

    def _recalculateCategorizedSummary(self):
        self.categorized_summary[MonthSummary.NECESSITY] = self.categorized_revenue[MonthSummary.NECESSITY] + self.categorized_expense[MonthSummary.NECESSITY]
        self.categorized_summary[MonthSummary.NICE] = self.categorized_revenue[MonthSummary.NICE] + self.categorized_expense[MonthSummary.NICE]
        self.categorized_summary[MonthSummary.SAVING] = self.categorized_revenue[MonthSummary.SAVING] + self.categorized_expense[MonthSummary.SAVING]

    def sort(self):
        self.revenues = sorted(self.revenues)
        self.expenses = sorted(self.expenses, reverse=True)