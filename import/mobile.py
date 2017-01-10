#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

CURRENCY_CZK = 1
SOURCE_VALET = 1

from service.repository import Repository

class TypeResolver:
    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()
        self.types = {}
        
    def resolve(self, name):
        types = self._getTypes()
        name = self._formatTypeName(name)
        
        if name in types:
            return types[name]
        else:
            raise Exception('Typ "{0}" není v databázi.'.format(name))
    
    def _getTypes(self):
        if len(self.types) > 0:
            return self.types
        
        self.cursor.execute('SELECT id, name FROM reports_recordtype ORDER BY id')
        for type in self.cursor.fetchall():
            self.types[self._formatTypeName(type[1])] = type[0]
        
        return self.types
    
    def _formatTypeName(self, name):
        replacements = {
            'ě' : 'e',
            'š' : 's',
            'č' : 'c',
            'ř' : 'r',
            'ž' : 'z',
            'ý' : 'y',
            'á' : 'a',
            'í' : 'i',
            'é' : 'e',
            'ú' : 'u',
            'ů' : 'u',
        }
        
        name = name.lower()
        for replace, replacement in replacements.items():
            name = name.replace(replace, replacement)

        return name
    
        

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
    reader = csv.reader(file, delimiter=';')
    print('Soubor byl úspěšně otevřen, zahajuji zpracovávání CSV')
    for row in reader:
        if len(row) < 2:
            continue
        
        if row[0] != '' and row[0] != None:
            match = re.search(r'([0-9]+)\.([0-9]+)\.', row[0])
            if match != None:
                date = datetime.strptime(year + match.group(2) + match.group(1), '%Y%m%d')
                date = date.replace(hour=0, minute=0, second=0)
        
        if len(row) < 5:
            raise Exception('Řádek s popisem "{0}" nemá dostatek hodnot'.format(row[2]))
        
        records.append({
            'date' : date,
            'money' : int(row[1]),
            'currency' : CURRENCY_CZK,
            'description' : row[2],
            'place' : row[3],
            'type' : resolver.resolve(row[4]),
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