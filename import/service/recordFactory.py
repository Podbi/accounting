import re

CURRENCY_CZK = 1
SOURCE_VALET = 1
SOURCE_BANK = 2
SOURCE_HOME = 3

class RecordFactory:
    def create(self, row, date):
        records = []
        if (row['bank'] != ''):
            records.append(
                self._createRecord(
                    row,
                    date, 
                    row['bank'],
                    SOURCE_BANK
                )
            )
        if (row['valet'] != ''):
            records.append(
                self._createRecord(
                    row,
                    date, 
                    row['valet'],
                    SOURCE_VALET
                )
            )
        elif (row['home'] != ''):
            records.append(
                self._createRecord(
                    row,
                    date, 
                    row['home'],
                    SOURCE_HOME
                )
            )
        
        return records
    
    def _createRecord(self, row, date, money, source):
        money = re.match(r"(\-?[0-9 ]+)([A-Za-zěščřžýáíé]+)", money)
        if money.group(2).strip() == 'Kč':
            currency = CURRENCY_CZK
        else:
            raise Error('Neočekávaná měna' + money.group(2).strip().replace(' ', ''))
        return {
            'date' : date,
            'money' : float(money.group(1).strip().replace(' ', '')),
            'currency': currency,
            'description' : row['description'],
            'type' : row['type'],
            'source' : source,
            'category' : row['category']
        }
