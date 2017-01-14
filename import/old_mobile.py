#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re

CURRENCY_CZK = 1
SOURCE_VALET = 1

if len(sys.argv) < 2:
    raise Exception('Málo vstupních argumentů. Zadej název souboru.')

date = ''
records = []
filepath = sys.argv[1]

print('Soubor',filepath,'bude otevřen a zpracován')
with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
    lines = file.readlines()
print('Soubor byl úspěšně otevřen, zahajuji zpracovávání obsahu')
for line in lines:
    match = re.match(r'([0-9]+\.[0-9]+\.)?( )?(\-?[0-9]+)([ 0-9a-zA-Z,.]+)\(([ 0-9a-zA-Z,.]+)\)', line)
    if match != None:

        if match.group(1) != None:
            date = match.group(1)
            
        if match.group(4) == None:
            raise Exception('Řádek s popisem "{0}" nemá dostatek hodnot'.format(match.group(4)))
        
        print('.', end='')
        
        records.append([
            date,
            match.group(3),
            match.group(4).strip(),
            match.group(5),
            None,
        ])

print('')
print('Celkem bylo nalezeno',len(records),'záznamů, které budou exportovány do CSV souboru')

with open('mobile.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Import'])
    for record in records:
        writer.writerow(record)
        
print('CSV soubor s názvem "mobile.csv" byl úspěšně vytvořen.')