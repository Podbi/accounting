class SummaryRecord:
    def __init__(self, type, name, amount, currency):
        self.type = type
        self.name = name
        self.amount = round(amount, 0)
        self.currency = currency
        
    def __repr__(self):
        return '{} - {} {}'.format(self.name, self.amount,self.currency)
        
    def __lt__(self, other):
        return self.amount > other.amount
        
    def __eq__(self, other):
        return self.amount == other.amount