import calendar
from datetime import datetime
from django.db import connection
from django.urls import reverse
from _datetime import date
from _codecs import code_page_decode

class MonthTranslator:
    def __init__(self):
        self.months = {
            1 : 'Leden',
            2 : 'Únor',
            3 : 'Březen',
            4 : 'Duben',
            5 : 'Květen',
            6 : 'Červen',
            7 : 'Červenec',
            8 : 'Srpen',
            9 : 'Září',
            10 : 'Říjen',
            11 : 'Listopad',
            12 : 'Prosinec',
        }
    
    def translate(self, month):
        return self.months[month]

class MonthSummaryCalculator:
    def calculate(self, dateFrom, dateTo, currency):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(record.money), currency.code, type.id, type.name 
                FROM reports_record AS record 
                JOIN reports_currency AS currency ON record.currency_id = currency.id 
                JOIN reports_recordtype AS type ON record.type_id = type.id 
                WHERE record.date >= %s AND record.date <= %s AND currency.code = %s
                GROUP BY currency.code, type.id, type.name 
                ORDER BY type.name
                """,
                (
                    dateFrom.strftime('%Y-%m-%d %H:%M:%S'),
                    dateTo.strftime('%Y-%m-%d %H:%M:%S'),
                    currency
                )
            )
            rows = cursor.fetchall()
        
        summary = MonthSummary(currency)
        for row in rows:
            record = SummaryRecord(row[2], row[3], row[0], row[1])
            if record.amount > 0:
                summary.addRevenue(record)
            elif record.amount < 0:
                summary.addExpense(record)
        summary.sort()
        
        return summary

    def listOfAvailable(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT substr(date, 0, 5) AS year, substr(date, 6, 2) AS month 
                FROM reports_record 
                ORDER BY year, month
            """
            )
            rows = cursor.fetchall()
        translator = MonthTranslator()
        months = []
        for row in rows:
            months.append({
                'url' : reverse('record:month_summary', kwargs={'month': row[1], 'year' : row[0]}),
                'label' : translator.translate(int(row[1])) + ' ' + row[0]
            })
        
        return months

class MonthSummary:
    def __init__(self, currency):
        self.currency = currency
        self.revenues = []
        self.expenses = []
        self.revenue = 0.00;
        self.expense = 0.00;
        self.summary = 0.00;
        
    def addRevenue(self, record):
        self.revenues.append(record)
        self.revenue += record.amount
        self.summary = self.revenue + self.expense
        
    def addExpense(self, record):
        self.expenses.append(record)
        self.expense += record.amount
        self.summary = self.revenue + self.expense
        
    def sort(self):
        self.revenues = sorted(self.revenues)
        self.expenses = sorted(self.expenses, reverse=True)
    

class SummaryRecord:
    def __init__(self, type, name, amount, currency):
        self.type = type
        self.name = name
        self.amount = amount
        self.currency = currency
        
    def __repr__(self):
        return '{} - {} {}'.format(self.name, self.amount,self.currency)
        
    def __lt__(self, other):
        return self.amount > other.amount
        
    def __eq__(self, other):
        return self.amount == other.amount

class DateFactory:
    def createFirstDayOfMonth(self, month, year):
        date = self._createDate('01', month, year)
        date = date.replace(hour=0, minute=0, second=0)
        
        return date
    
    def createLastDayOfMonth(self, month, year):
        date = self._createDate(calendar.monthrange(year, month)[1], month, year)
        date = date.replace(hour=23, minute=59, second=59)
        
        return date
        
    def _createDate(self, day, month, year):
        return datetime.strptime(str(day) + str(month) + str(year), '%d%m%Y')
    
class Record:
    def __init__(self, id, date, description, place, type, money, currency, source):
        self.id = id
        self.date = date
        self.description = description
        self.place = place
        self.type = type
        self.money = money
        self.currency = currency
        self.source = source
    
class RecordTypeRepository:
    def findAllByTypeAndDates(self, type, dateFrom, dateTo, currency):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    record.id,
                    record.date,
                    record.description,
                    record.place,
                    type.name AS type,
                    record.money,
                    currency.code AS currency,
                    source.name AS source
                FROM reports_record AS record 
                JOIN reports_currency AS currency ON record.currency_id = currency.id 
                JOIN reports_recordtype AS type ON record.type_id = type.id
                JOIN reports_moneysource AS source ON record.source_id = source.id 
                WHERE record.date >= %s AND record.date <= %s AND currency.code = %s AND type.id = %s
                ORDER BY record.date DESC
                """,
                (
                    dateFrom.strftime('%Y-%m-%d %H:%M:%S'),
                    dateTo.strftime('%Y-%m-%d %H:%M:%S'),
                    currency,
                    type
                )
            )
            rows = cursor.fetchall()
        
        records = []
        for row in rows:
            records.append(
                Record(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
           )
        
        return records
    
class RecordByMonthRepository:
    def findAllByDates(self, dateFrom, dateTo, currency):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    record.id,
                    record.date,
                    record.description,
                    record.place,
                    type.name AS type,
                    record.money,
                    currency.code AS currency,
                    source.name AS source
                FROM reports_record AS record 
                JOIN reports_currency AS currency ON record.currency_id = currency.id 
                JOIN reports_recordtype AS type ON record.type_id = type.id
                JOIN reports_moneysource AS source ON record.source_id = source.id 
                WHERE record.date >= %s AND record.date <= %s AND currency.code = %s
                ORDER BY record.date DESC
                """,
                (
                    dateFrom.strftime('%Y-%m-%d %H:%M:%S'),
                    dateTo.strftime('%Y-%m-%d %H:%M:%S'),
                    currency
                )
            )
            rows = cursor.fetchall()
        
        records = []
        for row in rows:
            records.append(
                Record(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
           )
        
        return records