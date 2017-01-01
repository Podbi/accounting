#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

SOURCE_VALET = 1
SOURCE_BANK = 2
SOURCE_HOME = 3
CURRENCY_CZK = 1

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
            raise Error('Neočekávaná měna' + money.group(2).strip())
        return {
            'date' : date,
            'money' : money.group(1).strip(),
            'currency': currency,
            'description' : row['description'],
            'type' : row['type'],
            'source' : source
        }


if len(sys.argv) < 2:
    raise Exception('Málo vstupních argumentů. Zadej název souboru')

database = sqlite3.connect('../db.sqlite3')

factory = RecordFactory()
date = ''
records = []
filepath = sys.argv[1]
print('Soubor',filepath,'bude otevřen a zpracován')
with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
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
    cursor = database.cursor()
    cursor.execute(
        'SELECT id FROM reports_record WHERE date = ? AND description = ? AND money = ? AND currency_id = ? AND source_id = ?',
        (
            record['date'],
            record['description'],
            record['money'],
            record['currency'],
            record['source']
            
        )
    )
    if (cursor.fetchone() == None):
        cursor.execute(
            'SELECT id FROM reports_recordtype WHERE name = ?',
            (record['type'],)
        )
        type = cursor.fetchone()
        if (type != None):
            record['type'] = type[0]
        else:
            print('')
            print('Vkládám nový typ záznamu',record['type'])
            cursor.execute(
                'INSERT INTO reports_recordtype(name) VALUES(?)',
                (record['type'],)
            )
            cursor.execute(
                'SELECT id FROM reports_recordtype WHERE name = ?',
                (record['type'],)
            )
            type = cursor.fetchone()
            record['type'] = type[0]
        cursor.execute(
            'INSERT INTO reports_record(date, description, money, currency_id, source_id, type_id) VALUES(?, ?, ?, ?, ?, ?)',
            (
                record['date'],
                record['description'],
                record['money'],
                record['currency'],
                record['source'],
                record['type']
            )
        )
        counter = counter + 1
        print('.', end='')
        
    else:
        print('Záznam ze dne', record['date'], 'za', record['money'], 'již existuje.')


database.commit()
database.close()
print('')
print(counter,'záznamů bylo úspěšně vloženo')
