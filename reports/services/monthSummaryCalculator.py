from django.db import connection
from django.urls import reverse

from .monthSummary import MonthSummary
from .summaryRecord import SummaryRecord
from .monthTranslator import MonthTranslator

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