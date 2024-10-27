class SummaryRecord:
    def __init__(self, type, name, amount, necessity_amount, nice_amount, saving_amount, currency):
        self.type = type
        self.name = name
        self.amount = round(amount, 0)
        self.necessity_amount = round(necessity_amount, 0) if necessity_amount is not None else None
        self.nice_amount = round(nice_amount, 0) if nice_amount is not None else None
        self.saving_amount = round(saving_amount, 0) if saving_amount is not None else None
        self.currency = currency
        
    def __repr__(self):
        return '{} - {} {}'.format(self.name, self.amount, self.currency)
        
    def __lt__(self, other):
        return self.amount > other.amount
        
    def __eq__(self, other):
        return self.amount == other.amount