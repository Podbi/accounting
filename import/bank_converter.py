#  -*- coding: utf-8 -*-
from datetime import datetime
import sys
import csv
import sqlite3
import re
from _datetime import date

CURRENCY_CZK = 1
SOURCE_VALET = 1

if len(sys.argv) < 2:
    raise Exception('Málo vstupních argumentů. Zadej název souboru.')

date = ''
records = []
filepath = sys.argv[1]

class KnownPaymentsResolver:
    def resolve(self, date, amount):
        if amount == '-5000,00':
            return self.createRecord(
                date,
                amount,
                'Monice na bydlení',
                'Monika Podborská',
                'pujceni penez'
            )
        elif amount == '-1823,00':
            return self.createRecord(
                date,
                amount,
                'Měsíční Zdravotní Pojištění',
                'VOZP, Brno',
                'pracovni vydaj'
            )
        elif amount == '-1972,00':
            return self.createRecord(
                date,
                amount,
                'Měsíční Sociální Zabezpečení',
                'MSSZ, Brno',
                'pracovni vydaj'
            )
        elif amount == '-1000,00':
            return self.createRecord(
                date,
                amount,
                'Stavební spoření',
                'Trvalý příkaz (ČMSS)',
                'stavebni sporeni'
            )
        elif amount == '-300,00':
            return self.createRecord(
                date,
                amount,
                'Penzijní připojištění',
                'Trvalý příkaz (ČMSS)',
                'penzijni pripojisteni'
            )
        elif amount == '-797,00':
            return self.createRecord(
                date,
                amount,
                'Životní pojištění MetLife',
                'MetLife',
                'zivotni pojisteni'
            )
        elif amount == '-2000,00':
            return self.createRecord(
                date,
                amount,
                'Investnční vklad',
                'Investice Conseq',
                'investice'
            )
        elif amount == '-845,00':
            return self.createRecord(
                date,
                amount,
                'Povinné ručení za Ford C-MAX',
                'Česká pojišťovna',
                'doprava'
            )
        elif amount == '-728,00':
            return self.createRecord(
                date,
                amount,
                'NETBOX Internet + TV',
                'Uzbecká, Brno',
                'bydleni'
            )
        elif amount == '-9,00':
            return self.createRecord(
                date,
                amount,
                'Poplatek za výběr z bankomatu',
                'KB - Platební účet',
                'bankovni poplatek'
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

resolver = KnownPaymentsResolver()

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

        record = resolver.resolve(date, amount)
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