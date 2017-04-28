#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

from service.repository import Repository
from service.recordFactory import RecordFactory

if len(sys.argv) < 2:
    raise Exception('Málo vstupních argumentů. Zadej název souboru')

factory = RecordFactory()
repository = Repository(sqlite3.connect('../db.sqlite3'))
date = ''
records = []
filepath = sys.argv[1]
print('Soubor',filepath,'bude otevřen a zpracován')
with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as file:
    reader = csv.reader(file, delimiter=';')
    print('Soubor byl úspěšně otevřen, zahajuji zpracovávání CSV')
    for row in reader:
        print('.', end='')
        row = {
            'date': row[0],
            'bank': row[1],
            'valet': row[2],
            'home': row[3],
            'description': row[6],
            'type': row[9]
        }
        if (row['description'] == ''):
            continue
        if (row['date'] != ''):
            date = datetime.strptime(row['date'], '%d.%m.%Y')
            date = date.replace(hour=0, minute=0, second=0)
        
        for record in factory.create(row, date):
            records.append(record)

print('')
print('Celkem bylo nalezeno',len(records),'záznamů, které budou vloženy do databáze')
print('Vkládám záznamy')
counter = 0
for record in records:
    if (repository.hasRecord(record['date'], record['description'], record['money'], record['currency'], record['source'])):
        print('Záznam ze dne', record['date'], 'za', record['money'], 'již existuje.')
    else:
        type = repository.getType(record['type'])
        if (type != None):
            record['type'] = type
        else:
            print('')
            print('Vkládám nový typ záznamu',record['type'])
            record['type'] = repository.createType(record['type'])
        repository.createRecord(
            record['date'],
            record['description'],
            None,
            record['money'],
            record['currency'],
            record['source'],
            record['type']
        )
        counter = counter + 1
        print('.', end='')
        
repository.commit()
print('')
print(counter,'záznamů bylo úspěšně vloženo')
