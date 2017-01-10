#  -*- coding: utf-8 -*-
import sqlite3
from service.repository import Repository

repository = Repository(sqlite3.connect('../db.sqlite3'))
rows = repository.findAll()

print('Nalezeno celkem', len(rows), 'záznamů k aktualizaci "místa"')

for row in rows:
    start = row[1].find('(')
    if start == -1:
        continue
    end = row[1].find(')', start)
    if end == -1:
        continue
    
    print('.', end='')
    
    description = row[1][0:start - 1]
    place = row[1][start + 1:end]
    
    repository.update(row[0], description, place)

repository.commit()
print('')
print('Záznamy byly úspěšně aktualizovány')
