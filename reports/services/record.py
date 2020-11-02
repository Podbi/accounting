class Record:
    def __init__(self, id, date, description, place, type, money, currency, source):
        self.id = id
        self.date = date
        self.description = description
        self.place = place
        self.type = type
        self.money = round(money, 0)
        self.currency = currency
        self.source = source