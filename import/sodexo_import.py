#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

CURRENCY_CZK = 1
SOURCE_VALET = 1

from service.repository import Repository
from service.typeResolver import TypeResolver

if len(sys.argv) < 3:
    raise Exception('Málo vstupních argumentů. Zadej název souboru a rok')

date = ''
records = []
filepath = sys.argv[1]
year = sys.argv[2]
database = sqlite3.connect('../db.sqlite3')
resolver = TypeResolver(database)
repository = Repository(database)

print('Soubor',filepath,'bude otevřen a zpracován')
with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
    reader = csv.reader(file, delimiter='\t')
    print('Soubor byl úspěšně otevřen, zahajuji zpracovávání textového souboru')
    for row in reader:
        if len(row) < 2:
            continue
        
        if row[1] != '' and row[1] != None:
            match = re.search(r'([0-9]+)\.([0-9]+)\.', row[1])
            if match != None:
                date = datetime.strptime(row[1], '%d.%m.%Y %H:%M:%S')
                date = date.replace(hour=0, minute=0, second=0)
        
        if len(row) < 5:
            raise Exception('Řádek s popisem "{0}" nemá dostatek hodnot'.format(row[3]))
        
        match = re.search(r'(\-)?[0-9]+', row[0])
        if match != None:
            money = match.group(0)
        else:
            raise Exception('Řádek s popisem "{0}" neobsahuje validní údaje o měně: "{1}"'.format(row[3], row[0]))

        description = 'Oběd (Stravování)'
        place = row[3].capitalize()
        if place == '' and int(money) > 0:
            description = 'Měsíční Stravenky'
            place = 'Dixons Carphone CoE'
        
        records.append({
            'date' : date,
            'money' : int(money),
            'currency' : CURRENCY_CZK,
            'description' : description,
            'place' : place,
            'type' : resolver.resolve('stravovani'),
            'source' : SOURCE_VALET
        })

print('')
print('Celkem bylo nalezeno',len(records),'záznamů, které budou vloženy do databáze')
print('Vkládám záznamy')

counter = 0
for record in records:
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
            record['type']
        )
        counter = counter + 1
        print('.', end='')
        
repository.commit()
print('')
print(counter,'záznamů bylo úspěšně vloženo')