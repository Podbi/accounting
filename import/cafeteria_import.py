#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

CURRENCY_CZK = 1
SOURCE_BANK = 2

from service.repository import Repository
from service.typeResolver import TypeResolver

if len(sys.argv) < 2:
    raise Exception('Málo vstupních argumentů. Zadej název souboru')

date = ''
records = []
filepath = sys.argv[1]
database = sqlite3.connect('../db.sqlite3')
resolver = TypeResolver(database)
repository = Repository(database)

def shouldNotBeSkipped(description):
    match = re.search(r'Dixons CarphoneSalary Swap', description)
    if match != None:
        return False
    return True

def formatDate(date):
    match = re.search(r'([0-9]+)\.([0-9]+)\.([0-9]{4})', date)
    if match != None:
        month = match.group(2)
        if len(month) != 2:
            month = "0" + month
        date = datetime.strptime(match.group(3) + month + match.group(1), '%Y%m%d')
        return date.replace(hour=0, minute=0, second=0)
    else:
        match = re.search(r'([0-9]+)/([0-9]+)/([0-9]{4})', date)
        if match != None:
            date = datetime.strptime(match.group(3) + match.group(2) + match.group(1), '%Y%m%d')
            return date.replace(hour=0, minute=0, second=0)
    raise Exception('Datum "{0}" není ve správném formátu.'.format(date))

def extractDescription(description):
    match = re.search(r'(Food and Drink|Food and drink|Food)[ ]+(.+)', description)
    if match != None:
        return match.group(2)
    return None

def formatDescription(description):
    extraction = extractDescription(description)
    if extraction != None:
        return 'Stravování (' + extraction + ')'
    return ' '.join(description.split())

def formatAmount(amount):
    amount = amount.replace(u'\xa0', u' ')
    match = re.search(r'((-)?[0-9 ]+\,[0-9]*)', amount)
    if match != None:
        return float(match.group(1).replace(',','.').replace(' ',''))
    raise Exception('Částka "{0}" není ve správném formátu.'.format(amount))

def formatPlace(description, place):
    extraction = extractDescription(description)
    if extraction != None:
        return extraction
    return place


def resolveType(amount):
    if amount > 0.0 :
        return resolver.resolve('vyplata')
    return resolver.resolve('stravovani')

print('Soubor',filepath,'bude otevřen a zpracován')
with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
    reader = csv.reader(file, delimiter=';')
    print('Soubor byl úspěšně otevřen, zahajuji zpracovávání CSV')

    next(reader)
    for row in reader:

        if len(row) < 5:
            raise Exception('Řádek s popisem "{0}" nemá dostatek hodnot'.format(row[3]))

        if shouldNotBeSkipped(row[2]) :
            records.append({
                'date' : formatDate(row[1]),
                'money' : formatAmount(row[4]),
                'currency' : CURRENCY_CZK,
                'description' : formatDescription(row[2]),
                'place' : formatDescription(row[2]),
                'type' : resolveType(formatAmount(row[4])),
                'source' : SOURCE_BANK
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