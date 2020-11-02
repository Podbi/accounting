#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re
from _datetime import date
from data.knownPayments import knownPayments

CURRENCY_CZK = 1
SOURCE_VALET = 1

if len(sys.argv) < 2:
    raise Exception('Málo vstupních argumentů. Zadej název souboru.')

date = ''
records = []
filepath = sys.argv[1]

class KnownPaymentsResolver:

    def __init__(self, knownPayments):
        self._knownPayments = knownPayments

    def resolve(self, date, amount, row):
        record = self._resolvePaymentByAmount(date, amount)
        if record:
            return record
        record = self._resolvePaymentByIssuerNote(date, amount, row[15])
        if record:
            return record

        return None

    def _resolvePaymentByAmount(self, date, amount):
        for knownPayment in self._knownPayments:
            if amount == knownPayment['amount']:
                return self.createRecord(
                    date,
                    amount,
                    knownPayment['description'],
                    knownPayment['place'],
                    knownPayment['type']
                )

        return None

    def _resolvePaymentByIssuerNote(self, date, amount, note):
       for knownPayment in self._knownPayments:
           if 'note' in knownPayment and note.lower().startswith(knownPayment['note'].lower()):
               return self.createRecord(
                   date,
                   amount,
                   knownPayment['description'],
                   knownPayment['place'],
                   knownPayment['type']
               )

       return None
    
    def createRecord(self, date, amount, description, place, type):
        return [
            date,
            self.convertAmount(amount),
            description,
            place,
            type
        ]
        
    def convertAmount(self, amount):
        return int(float(amount.replace(',', '.').replace('+', '')))

resolver = KnownPaymentsResolver(knownPayments)

print('Soubor',filepath,'bude otevřen a zpracován')
with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
    reader = csv.reader(file, delimiter=';')
    print('Soubor byl úspěšně otevřen, zahajuji zpracovávání CSV')
    for row in reader:
        if len(row) < 10:
            continue
        match = re.match(r'^[0-9]{2}\.[0-9]{2}\.', row[0])
        if match == None:
            continue
        print('.', end='')
        
        date = match.group(0)
        amount = row[4]

        record = resolver.resolve(date, amount, row)
        if record != None:
            records.append(record)
        else:
            records.append(
                resolver.createRecord(
                    date,
                    amount,
                    row[13],
                    row[3],
                    None,
                )
            )

print('')
print('Celkem bylo nalezeno',len(records),'záznamů, které budou exportovány do CSV souboru')

with open('bank.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Import'])
    for record in records:
        writer.writerow(record)
        
print('CSV soubor s názvem "bank.csv" byl úspěšně vytvořen.')