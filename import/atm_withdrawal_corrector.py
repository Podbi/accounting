#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

ATM_WITHDRAW_TYPE = 23
CURRENCY_CZK = 1
SOURCE_VALET = 1
PLACE_BANK = 'Komerční banka'

from service.repository import Repository
from service.recordFactory import RecordFactory

def findMatchingRecord(records, date, money):
    for record in records:
        if record['date'] == date and record['money'] == (money * -1):
            return record
    return None

database = sqlite3.connect('../db.sqlite3')
repository = Repository(database)

records = repository.findAllByType(ATM_WITHDRAW_TYPE)

for index, record in enumerate(records):
    records[index] = {
        'date' : datetime.strptime(record[0][:10], '%Y-%m-%d').date(),
        'description' : record[1],
        'money' : record[2],
        'source' : record[3]
    }

newRecords = []

for record in records:
    if record['money'] < 0:
        match = findMatchingRecord(records, record['date'], record['money'])
        if match is None:
            newRecords.append({
                'date' : record['date'],
                'money' : (record['money'] * -1),
                'currency': CURRENCY_CZK,
                'description' : record['description'],
                'place' : PLACE_BANK,
                'type' : ATM_WITHDRAW_TYPE,
                'source' : SOURCE_VALET,
                'category' : None
            })

print('')
print('Celkem bude doplněno',len(newRecords),'záznamů, které budou vloženy do databáze')
print('Vkládám záznamy')
counter = 0
for record in newRecords:
    if (repository.hasRecord(record['date'], record['description'], record['money'], record['currency'], record['source'])):
        print('Záznam ze dne', record['date'], 'za', record['money'], 'již existuje.')
    else:
        repository.createRecord(
            record['date'],
            record['description'],
            record['place'],
            record['money'],
            record['currency'],
            record['source'],
            record['type'],
            record['category']
        )
        counter = counter + 1
        print('.', end='')
        
repository.commit()
print('')
print(counter,'záznamů bylo úspěšně vloženo')
        